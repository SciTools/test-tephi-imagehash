from pathlib import Path
import unittest

from PIL import Image
import imagehash

import image_manifest


_HASH_SIZE = 16
# Ideally, a hamming distance of 2 is typically sufficient. However,
# we're relaxing this to 4 to accommodate the migration in behaviour
# of unpinning pillow<7.
_HAMMING_DISTANCE = 4


class TestHash(unittest.TestCase):
    def test(self):
        exceptions = []
        for fname in Path(".").glob("images/*.png"):
            phash = imagehash.phash(Image.open(fname), hash_size=_HASH_SIZE)
            fname_hash = imagehash.hex_to_hash(fname.stem)
            hamming = fname_hash - phash
            if hamming > _HAMMING_DISTANCE:
                msg = f'phash {phash} does not match {fname.name} [{hamming=}].'
                exceptions.append(ValueError(msg))
        self.assertEqual([], exceptions)


class TestManifest(unittest.TestCase):
    def test(self):
        image_fnames = set(image_manifest.image_fnames())
        manifest_fnames = set(image_manifest.manifest_fnames())

        if image_fnames != manifest_fnames:
            emsg = "\n\nMismatch between image manifest and repo images.\n"
            new = image_fnames - manifest_fnames
            missing = manifest_fnames - image_fnames
            if new:
                emsg += "Images in repo but not in manifest:\n\t"
                emsg += "\t".join([fname for fname in sorted(new)])
            if missing:
                emsg += "Images reference in manifest but not in repo:\n\t"
                emsg += "\t".join([fname for fname in sorted(missing)])
            emsg += '\n\nPlease manually execute the "image_manifest.py" script.'
            self.assertEqual(image_fnames, manifest_fnames, emsg)


if __name__ == "__main__":
    unittest.main()
