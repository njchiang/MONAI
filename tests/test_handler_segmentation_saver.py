# Copyright 2020 MONAI Consortium
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import shutil
import unittest
import torch
from ignite.engine import Engine

from monai.handlers.segmentation_saver import SegmentationSaver


class TestHandlerSegmentationSaver(unittest.TestCase):

    def test_saved_content(self):
        default_dir = os.path.join('.', 'tempdir')
        shutil.rmtree(default_dir, ignore_errors=True)

        # set up engine
        def _train_func(engine, batch):
            return torch.zeros(8, 1, 2, 2)

        engine = Engine(_train_func)

        # set up testing handler
        saver = SegmentationSaver(output_dir=default_dir, output_postfix='seg', output_ext='.nii.gz')
        saver.attach(engine)

        data = [{'filename_or_obj': ['testfile' + str(i) for i in range(8)]}]
        engine.run(data, max_epochs=1)
        for i in range(8):
            filepath = os.path.join('testfile' + str(i), 'testfile' + str(i) + '_seg.nii.gz')
            self.assertTrue(os.path.exists(os.path.join(default_dir, filepath)))
        shutil.rmtree(default_dir)


if __name__ == '__main__':
    unittest.main()
