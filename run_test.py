import glob
import os
import unittest

from PIL import Image
import imagehash

import image_manifest


_HASH_SIZE = 16


class TestHash(unittest.TestCase):
    def test(self):
        self.maxDiff = None
        exceptions = []
        for fname in glob.glob("images/*.png"):
            phash = imagehash.phash(Image.open(fname), hash_size=_HASH_SIZE)
            fname_base = os.path.basename(fname)
            fname_hash = os.path.splitext(fname_base)[0]
            if str(phash) != fname_hash:
                msg = 'Calculated phash {} does not match filename {!r}.'
                exceptions.append(ValueError(msg.format(str(phash), fname_base)))
        self.assertEqual([], exceptions)


class TestManifest(unittest.TestCase):
    def test(self):
        image_fnames = set(image_manifest.image_fnames())
        manifest_fnames = set(image_manifest.manifest_fnames())

        if image_fnames != manifest_fnames:
            emsg = "Mismatch between image manifest and repo images.\n"
            new = image_fnames - manifest_fnames
            missing = manifest_fnames - image_fnames
            if new:
                emsg += "Images in repo but not in manifest:\n\t"
                emsg += "\t".join([fname for fname in sorted(new)])
            if missing:
                emsg += "Images reference in manifest but not in repo:\n\t"
                emsg += "\t".join([fname for fname in sorted(missing)])
            emsg += '\n\nPlease manually execute the "image_manifest.py" script.'
            self.assertEqual(image_files, manifest_fnames, emsg)


if __name__ == "__main__":
    unittest.main()
