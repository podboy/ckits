#!/usr/bin/python3
# coding:utf-8

import unittest

from ckits_images import tags


class TestTag(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tag = "v1.0.0"
        cls.digest = "sha256:a8560b36e8b8210634f77d9f7f9efd7ffa463e380b75e2e74aff4511df3ef88c"  # noqa:E501
        cls.repository = "demo"
        cls.namespace = "unittest"
        cls.registry_host = "registry.example.com"
        cls.name_without_tag = f"{cls.registry_host}/{cls.namespace}/{cls.repository}"  # noqa:E501
        cls.name_latest_tag = f"{cls.name_without_tag}:{tags.Tag.LATEST_TAG}"  # noqa:E501
        cls.name_stable_tag = f"{cls.name_without_tag}:{tags.Tag.STABLE_TAG}"  # noqa:E501
        cls.name = f"{cls.registry_host}/{cls.namespace}/{cls.repository}:{cls.tag}"  # noqa:E501

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_tag_init(self):
        self.assertRaises(ValueError, tags.Tag, "demo", extra_tags=[tags.Tag.STABLE_TAG])  # noqa:E501
        self.assertRaises(ValueError, tags.Tag, "demo", tag=self.tag, digest=self.digest)  # noqa:E501

    def test_tag_eq(self):
        self.assertNotEqual(tags.Tag("demo"), f"demo:{tags.Tag.STABLE_TAG}")
        self.assertEqual(tags.Tag("demo"), f"demo:{tags.Tag.LATEST_TAG}")
        self.assertFalse(tags.Tag("demo") == tags.Tags())

    def test_is_extra_tag(self):
        self.assertIsInstance(tag := tags.Tag("demo", tag=self.tag, extra_tags=[tags.Tag.STABLE_TAG]), tags.Tag)  # noqa:E501
        self.assertFalse(tag.is_extra_tag(f"demo:{tags.Tag.LATEST_TAG}"))
        self.assertTrue(tag.is_extra_tag(f"demo:{tags.Tag.STABLE_TAG}"))

    def test_parse_repository_name(self):
        self.assertRaises(ValueError, tags.Tag.parse, "a+b=c")

    def test_parse_error_digest(self):
        self.assertRaises(ValueError, tags.Tag.parse, f"{self.repository}@sha123:a8560b36e8b8210634f77d9f7f9efd7ffa463e380b75e2e74aff4511df3ef88c")  # noqa:E501
        self.assertRaises(ValueError, tags.Tag.parse, f"{self.repository}@sha256:54321")  # noqa:E501

    def test_parse_repository(self):
        self.assertIsInstance(tag := tags.Tag.parse(self.repository), tags.Tag)  # noqa:E501
        self.assertEqual(tag.registry_host, tags.Tag.DEFAULT_REGISTRY_HOST)
        self.assertEqual(tag.namespace, tags.Tag.DEFAULT_NAMESPACE)
        self.assertEqual(tag.repository, self.repository)
        self.assertEqual(tag.tag, tags.Tag.LATEST_TAG)
        self.assertIsInstance(tag.extra_tags, tags.Tags)
        self.assertIsNone(tag.digest)
        self.assertEqual(tag.image, f"{self.repository}:{tags.Tag.LATEST_TAG}")
        self.assertEqual(tag.name_without_tag, f"{tags.Tag.DEFAULT_REGISTRY_HOST}/{tags.Tag.DEFAULT_NAMESPACE}/{self.repository}")  # noqa:E501
        self.assertEqual(tag.name_latest_tag, f"{tags.Tag.DEFAULT_REGISTRY_HOST}/{tags.Tag.DEFAULT_NAMESPACE}/{self.repository}:{tags.Tag.LATEST_TAG}")  # noqa:E501
        self.assertEqual(tag.name_stable_tag, f"{tags.Tag.DEFAULT_REGISTRY_HOST}/{tags.Tag.DEFAULT_NAMESPACE}/{self.repository}:{tags.Tag.STABLE_TAG}")  # noqa:E501
        self.assertEqual(tag.name, f"{tags.Tag.DEFAULT_REGISTRY_HOST}/{tags.Tag.DEFAULT_NAMESPACE}/{self.repository}:{tags.Tag.LATEST_TAG}")  # noqa:E501
        self.assertEqual(str(tag), f"{tags.Tag.DEFAULT_REGISTRY_HOST}/{tags.Tag.DEFAULT_NAMESPACE}/{self.repository}:{tags.Tag.LATEST_TAG}")  # noqa:E501

    def test_parse_repository_tag(self):
        self.assertIsInstance(tag := tags.Tag.parse(f"{self.repository}:{self.tag}"), tags.Tag)  # noqa:E501
        self.assertEqual(tag.registry_host, tags.Tag.DEFAULT_REGISTRY_HOST)
        self.assertEqual(tag.namespace, tags.Tag.DEFAULT_NAMESPACE)
        self.assertEqual(tag.repository, self.repository)
        self.assertEqual(tag.tag, self.tag)
        self.assertIsInstance(tag.extra_tags, tags.Tags)
        self.assertIsNone(tag.digest)
        self.assertEqual(tag.image, f"{self.repository}:{self.tag}")
        self.assertEqual(tag.name_without_tag, f"{tags.Tag.DEFAULT_REGISTRY_HOST}/{tags.Tag.DEFAULT_NAMESPACE}/{self.repository}")  # noqa:E501
        self.assertEqual(tag.name_latest_tag, f"{tags.Tag.DEFAULT_REGISTRY_HOST}/{tags.Tag.DEFAULT_NAMESPACE}/{self.repository}:{tags.Tag.LATEST_TAG}")  # noqa:E501
        self.assertEqual(tag.name_stable_tag, f"{tags.Tag.DEFAULT_REGISTRY_HOST}/{tags.Tag.DEFAULT_NAMESPACE}/{self.repository}:{tags.Tag.STABLE_TAG}")  # noqa:E501
        self.assertEqual(tag.name, f"{tags.Tag.DEFAULT_REGISTRY_HOST}/{tags.Tag.DEFAULT_NAMESPACE}/{self.repository}:{self.tag}")  # noqa:E501
        self.assertEqual(str(tag), f"{tags.Tag.DEFAULT_REGISTRY_HOST}/{tags.Tag.DEFAULT_NAMESPACE}/{self.repository}:{self.tag}")  # noqa:E501

    def test_parse_repository_digest(self):
        self.assertIsInstance(tag := tags.Tag.parse(f"{self.repository}@{self.digest}"), tags.Tag)  # noqa:E501
        self.assertEqual(tag.registry_host, tags.Tag.DEFAULT_REGISTRY_HOST)
        self.assertEqual(tag.namespace, tags.Tag.DEFAULT_NAMESPACE)
        self.assertEqual(tag.repository, self.repository)
        self.assertEqual(tag.tag, tags.Tag.LATEST_TAG)
        self.assertIsInstance(tag.extra_tags, tags.Tags)
        self.assertEqual(tag.digest, self.digest)
        self.assertEqual(tag.image, f"{self.repository}@{self.digest}")
        self.assertEqual(tag.name_without_tag, f"{tags.Tag.DEFAULT_REGISTRY_HOST}/{tags.Tag.DEFAULT_NAMESPACE}/{self.repository}")  # noqa:E501
        self.assertEqual(tag.name_latest_tag, f"{tags.Tag.DEFAULT_REGISTRY_HOST}/{tags.Tag.DEFAULT_NAMESPACE}/{self.repository}:{tags.Tag.LATEST_TAG}")  # noqa:E501
        self.assertEqual(tag.name_stable_tag, f"{tags.Tag.DEFAULT_REGISTRY_HOST}/{tags.Tag.DEFAULT_NAMESPACE}/{self.repository}:{tags.Tag.STABLE_TAG}")  # noqa:E501
        self.assertEqual(tag.name, f"{tags.Tag.DEFAULT_REGISTRY_HOST}/{tags.Tag.DEFAULT_NAMESPACE}/{self.repository}@{self.digest}")  # noqa:E501
        self.assertEqual(str(tag), f"{tags.Tag.DEFAULT_REGISTRY_HOST}/{tags.Tag.DEFAULT_NAMESPACE}/{self.repository}@{self.digest}")  # noqa:E501

    def test_parse_registry_host_repository(self):
        self.assertIsInstance(tag := tags.Tag.parse(f"{self.registry_host}/{self.repository}"), tags.Tag)  # noqa:E501
        self.assertEqual(tag.registry_host, self.registry_host)
        self.assertEqual(tag.namespace, tags.Tag.DEFAULT_NAMESPACE)
        self.assertEqual(tag.repository, self.repository)
        self.assertEqual(tag.tag, tags.Tag.LATEST_TAG)
        self.assertIsInstance(tag.extra_tags, tags.Tags)
        self.assertIsNone(tag.digest)
        self.assertEqual(tag.image, f"{self.repository}:{tags.Tag.LATEST_TAG}")
        self.assertEqual(tag.name_without_tag, f"{self.registry_host}/{tags.Tag.DEFAULT_NAMESPACE}/{self.repository}")  # noqa:E501
        self.assertEqual(tag.name_latest_tag, f"{self.registry_host}/{tags.Tag.DEFAULT_NAMESPACE}/{self.repository}:{tags.Tag.LATEST_TAG}")  # noqa:E501
        self.assertEqual(tag.name_stable_tag, f"{self.registry_host}/{tags.Tag.DEFAULT_NAMESPACE}/{self.repository}:{tags.Tag.STABLE_TAG}")  # noqa:E501
        self.assertEqual(tag.name, f"{self.registry_host}/{tags.Tag.DEFAULT_NAMESPACE}/{self.repository}:{tags.Tag.LATEST_TAG}")  # noqa:E501
        self.assertEqual(str(tag), f"{self.registry_host}/{tags.Tag.DEFAULT_NAMESPACE}/{self.repository}:{tags.Tag.LATEST_TAG}")  # noqa:E501

    def test_parse_namespace_repository(self):
        self.assertIsInstance(tag := tags.Tag.parse(f"{self.namespace}/{self.repository}"), tags.Tag)  # noqa:E501
        self.assertEqual(tag.registry_host, tags.Tag.DEFAULT_REGISTRY_HOST)
        self.assertEqual(tag.namespace, self.namespace)
        self.assertEqual(tag.repository, self.repository)
        self.assertEqual(tag.tag, tags.Tag.LATEST_TAG)
        self.assertIsInstance(tag.extra_tags, tags.Tags)
        self.assertIsNone(tag.digest)
        self.assertEqual(tag.image, f"{self.repository}:{tags.Tag.LATEST_TAG}")
        self.assertEqual(tag.name_without_tag, f"{tags.Tag.DEFAULT_REGISTRY_HOST}/{self.namespace}/{self.repository}")  # noqa:E501
        self.assertEqual(tag.name_latest_tag, f"{tags.Tag.DEFAULT_REGISTRY_HOST}/{self.namespace}/{self.repository}:{tags.Tag.LATEST_TAG}")  # noqa:E501
        self.assertEqual(tag.name_stable_tag, f"{tags.Tag.DEFAULT_REGISTRY_HOST}/{self.namespace}/{self.repository}:{tags.Tag.STABLE_TAG}")  # noqa:E501
        self.assertEqual(tag.name, f"{tags.Tag.DEFAULT_REGISTRY_HOST}/{self.namespace}/{self.repository}:{tags.Tag.LATEST_TAG}")  # noqa:E501
        self.assertEqual(str(tag), f"{tags.Tag.DEFAULT_REGISTRY_HOST}/{self.namespace}/{self.repository}:{tags.Tag.LATEST_TAG}")  # noqa:E501

    def test_parse_namespace_repository_tag(self):
        self.assertIsInstance(tag := tags.Tag.parse(f"{self.namespace}/{self.repository}:{self.tag}"), tags.Tag)  # noqa:E501
        self.assertEqual(tag.registry_host, tags.Tag.DEFAULT_REGISTRY_HOST)
        self.assertEqual(tag.namespace, self.namespace)
        self.assertEqual(tag.repository, self.repository)
        self.assertEqual(tag.tag, self.tag)
        self.assertIsInstance(tag.extra_tags, tags.Tags)
        self.assertIsNone(tag.digest)
        self.assertEqual(tag.image, f"{self.repository}:{self.tag}")
        self.assertEqual(tag.name_without_tag, f"{tags.Tag.DEFAULT_REGISTRY_HOST}/{self.namespace}/{self.repository}")  # noqa:E501
        self.assertEqual(tag.name_latest_tag, f"{tags.Tag.DEFAULT_REGISTRY_HOST}/{self.namespace}/{self.repository}:{tags.Tag.LATEST_TAG}")  # noqa:E501
        self.assertEqual(tag.name_stable_tag, f"{tags.Tag.DEFAULT_REGISTRY_HOST}/{self.namespace}/{self.repository}:{tags.Tag.STABLE_TAG}")  # noqa:E501
        self.assertEqual(tag.name, f"{tags.Tag.DEFAULT_REGISTRY_HOST}/{self.namespace}/{self.repository}:{self.tag}")  # noqa:E501
        self.assertEqual(str(tag), f"{tags.Tag.DEFAULT_REGISTRY_HOST}/{self.namespace}/{self.repository}:{self.tag}")  # noqa:E501

    def test_parse_registry_host_namespace_repository(self):
        self.assertIsInstance(tag := tags.Tag.parse(f"{self.registry_host}/{self.namespace}/{self.repository}"), tags.Tag)  # noqa:E501
        self.assertEqual(tag.registry_host, self.registry_host)
        self.assertEqual(tag.namespace, self.namespace)
        self.assertEqual(tag.repository, self.repository)
        self.assertEqual(tag.tag, tags.Tag.LATEST_TAG)
        self.assertIsInstance(tag.extra_tags, tags.Tags)
        self.assertIsNone(tag.digest)
        self.assertEqual(tag.image, f"{self.repository}:{tags.Tag.LATEST_TAG}")
        self.assertEqual(tag.name_without_tag, f"{self.registry_host}/{self.namespace}/{self.repository}")  # noqa:E501
        self.assertEqual(tag.name_latest_tag, f"{self.registry_host}/{self.namespace}/{self.repository}:{tags.Tag.LATEST_TAG}")  # noqa:E501
        self.assertEqual(tag.name_stable_tag, f"{self.registry_host}/{self.namespace}/{self.repository}:{tags.Tag.STABLE_TAG}")  # noqa:E501
        self.assertEqual(tag.name, f"{self.registry_host}/{self.namespace}/{self.repository}:{tags.Tag.LATEST_TAG}")  # noqa:E501
        self.assertEqual(str(tag), f"{self.registry_host}/{self.namespace}/{self.repository}:{tags.Tag.LATEST_TAG}")  # noqa:E501

    def test_parse_registry_host_namespace_repository_tag(self):
        self.assertIsInstance(tag := tags.Tag.parse(f"{self.registry_host}/{self.namespace}/{self.repository}:{self.tag}"), tags.Tag)  # noqa:E501
        self.assertEqual(tag.registry_host, self.registry_host)
        self.assertEqual(tag.namespace, self.namespace)
        self.assertEqual(tag.repository, self.repository)
        self.assertEqual(tag.tag, self.tag)
        self.assertIsInstance(tag.extra_tags, tags.Tags)
        self.assertIsNone(tag.digest)
        self.assertEqual(tag.image, f"{self.repository}:{self.tag}")
        self.assertEqual(tag.name_without_tag, f"{self.registry_host}/{self.namespace}/{self.repository}")  # noqa:E501
        self.assertEqual(tag.name_latest_tag, f"{self.registry_host}/{self.namespace}/{self.repository}:{tags.Tag.LATEST_TAG}")  # noqa:E501
        self.assertEqual(tag.name_stable_tag, f"{self.registry_host}/{self.namespace}/{self.repository}:{tags.Tag.STABLE_TAG}")  # noqa:E501
        self.assertEqual(tag.name, f"{self.registry_host}/{self.namespace}/{self.repository}:{self.tag}")  # noqa:E501
        self.assertEqual(str(tag), f"{self.registry_host}/{self.namespace}/{self.repository}:{self.tag}")  # noqa:E501


class TestTags(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_magic(self):
        tags_obj = tags.Tags()
        tags_obj.append("demo")
        tags_obj.extend([f"demo:{tags.Tag.LATEST_TAG}", f"demo:{tags.Tag.STABLE_TAG}"])  # noqa:E501
        self.assertEqual(len(tags_obj), 2)
        self.assertNotIn("test", tags_obj)
        self.assertIn("demo", tags_obj)
        for tag in tags_obj:
            self.assertIsInstance(tag, tags.Tag)
            self.assertEqual(tag.repository, "demo")

    def test_filter(self):
        self.assertIsInstance(tags_tuple := tags.Tags.filter(["demo", f"demo:{tags.Tag.LATEST_TAG}", f"demo:{tags.Tag.STABLE_TAG}"]), tuple)  # noqa:E501
        self.assertEqual(len(tags_tuple), 2)
        for tag in tags_tuple:
            self.assertIsInstance(tag, tags.Tag)
            self.assertEqual(tag.repository, "demo")


class TestTagConfigFile(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_load(self):
        from os.path import dirname
        from os.path import join
        base = dirname(dirname(dirname(__file__)))
        file = join(base, "example", "docker.io")
        self.assertIsInstance(tag_config := tags.TagConfigFile(file), tags.TagConfigFile)  # noqa:E501
        self.assertEqual(tag_config.dirname, join(base, "example"))
        self.assertEqual(tag_config.basename, "docker.io")
        self.assertEqual(tag_config.filename, file)
        self.assertRaises(FileNotFoundError, tags.TagConfigFile, join(base, "example", "library"))  # noqa:E501
        self.assertRaises(FileNotFoundError, tags.TagConfigFile, join(base, "example", "import"))  # noqa:E501
        self.assertRaises(FileNotFoundError, tags.TagConfigFile, join(base, "example"))  # noqa:E501
        self.assertRaises(ValueError, tags.TagConfigFile, join(base, "example", "docker"))  # noqa:E501


if __name__ == "__main__":
    unittest.main()
