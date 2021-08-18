

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"CheckNumberOfLevels/testsFiles/"

class TestCheckNumberOfLevels(unittest.TestCase):

    def test_1(self):
        """Test #1 : Test le plugin avec aucune option."""
        # open and read source
        source0 = plugin_test_dir + "input_big_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute CheckNumberOfLevels
        df = CheckNumberOfLevels(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [CheckNumberOfLevels]

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        assert(res)


    def test_2(self):
        """Test #2 : Test le plugin avec l'option 'minimum' égale à 3. Il doit retourné un message indiquant que le minimun n'est pas atteint!"""
        # open and read source
        source0 = plugin_test_dir + "input_big_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute CheckNumberOfLevels
        df = CheckNumberOfLevels(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [CheckNumberOfLevels --minimum 3]

        #write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        assert(res)


    def test_3(self):
        """Test #3 : Test le plugin avec l'option 'minimum' égale à -1. Il doit retourné un message indiquant que le minimun est invalide!"""
        # open and read source
        source0 = plugin_test_dir + "input_big_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute CheckNumberOfLevels
        df = CheckNumberOfLevels(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [CheckNumberOfLevels --minimum -1]

        #write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        assert(res)


    def test_4(self):
        """Test #4 : Test le plugin avec l'option 'minimum' égale à 1. Il doit indiquer aucun message!"""
        # open and read source
        source0 = plugin_test_dir + "input_big_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute CheckNumberOfLevels
        df = CheckNumberOfLevels(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [CheckNumberOfLevels --minimum 1]

        #write the result
        results_file = TMP_PATH + "test_4.std"
        StandardFileWriter(results_file, df)()

        assert(res)


    def test_5(self):
        """Test #5 : Test le plugin avec l'option 'maximum' égale à 11. Il doit indiquer aucun message!"""
        # open and read source
        source0 = plugin_test_dir + "input_big_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute CheckNumberOfLevels
        df = CheckNumberOfLevels(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName VV,UU --pdsLabel R1558V0N] >> [CheckNumberOfLevels --maximum 11]

        #write the result
        results_file = TMP_PATH + "test_5.std"
        StandardFileWriter(results_file, df)()

        assert(res)


    def test_6(self):
        """Test #6 : Test le plugin avec l'option 'maximum' égale à 1. Il doit retourné un message indiquant que le maximum est dépassé!"""
        # open and read source
        source0 = plugin_test_dir + "input_big_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute CheckNumberOfLevels
        df = CheckNumberOfLevels(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [CheckNumberOfLevels --maximum 1]

        #write the result
        results_file = TMP_PATH + "test_6.std"
        StandardFileWriter(results_file, df)()

        assert(res)


    def test_7(self):
        """Test #7 : Test le plugin avec l'option 'maximum' égale à 10. Il doit retourné un message indiquant que le maximum est dépassé!"""
        # open and read source
        source0 = plugin_test_dir + "input_big_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute CheckNumberOfLevels
        df = CheckNumberOfLevels(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName VV,UU --pdsLabel R1558V0N] >> [CheckNumberOfLevels --maximum 10]

        #write the result
        results_file = TMP_PATH + "test_7.std"
        StandardFileWriter(results_file, df)()

        assert(res)


    def test_8(self):
        """Test #8 : Test le plugin avec l'option 'maximum' égale à -1. Il doit retourné un message indiquant que le maximum est invalide!"""
        # open and read source
        source0 = plugin_test_dir + "input_big_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute CheckNumberOfLevels
        df = CheckNumberOfLevels(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName VV,UU --pdsLabel R1558V0N] >> [CheckNumberOfLevels --maximum -1]

        #write the result
        results_file = TMP_PATH + "test_8.std"
        StandardFileWriter(results_file, df)()

        assert(res)


    def test_9(self):
        """Test #9 : Test le plugin avec l'option 'exact' égale à 11. Il doit indiquer aucun message!"""
        # open and read source
        source0 = plugin_test_dir + "input_big_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute CheckNumberOfLevels
        df = CheckNumberOfLevels(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName VV,UU --pdsLabel R1558V0N] >> [CheckNumberOfLevels --exact 11]

        #write the result
        results_file = TMP_PATH + "test_9.std"
        StandardFileWriter(results_file, df)()

        assert(res)


    def test_10(self):
        """Test #10 : Test le plugin avec l'option 'exact' égale à 12. Il doit retourné un message indiquant que le nombre exact est pas atteint!"""
        # open and read source
        source0 = plugin_test_dir + "input_big_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute CheckNumberOfLevels
        df = CheckNumberOfLevels(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName VV,UU --pdsLabel R1558V0N] >> [CheckNumberOfLevels --exact 12]

        #write the result
        results_file = TMP_PATH + "test_10.std"
        StandardFileWriter(results_file, df)()

        assert(res)


    def test_11(self):
        """Test #11 : Test le plugin avec l'option 'exact' égale à 0. Il doit retourné un message indiquant que le nombre exact est pas atteint!"""
        # open and read source
        source0 = plugin_test_dir + "input_big_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute CheckNumberOfLevels
        df = CheckNumberOfLevels(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName VV,UU --pdsLabel R1558V0N] >> [CheckNumberOfLevels --exact 0]

        #write the result
        results_file = TMP_PATH + "test_11.std"
        StandardFileWriter(results_file, df)()

        assert(res)


    def test_12(self):
        """Test #12 : Test le plugin avec l'option 'exact' égale à -1. Il doit retourné un message indiquant que le nombre exact est invalide!"""
        # open and read source
        source0 = plugin_test_dir + "input_big_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute CheckNumberOfLevels
        df = CheckNumberOfLevels(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName VV,UU --pdsLabel R1558V0N] >> [CheckNumberOfLevels --exact -1]

        #write the result
        results_file = TMP_PATH + "test_12.std"
        StandardFileWriter(results_file, df)()

        assert(res)


    def test_13(self):
        """Test #13 : Test le plugin avec l'option 'exact' égale à 4. Il doit retourné un message indiquant que le nombre exact est pas atteint!!"""
        # open and read source
        source0 = plugin_test_dir + "input_big_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute CheckNumberOfLevels
        df = CheckNumberOfLevels(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName VV,UU --pdsLabel R1558V0N] >> [CheckNumberOfLevels --exact 4]

        #write the result
        results_file = TMP_PATH + "test_13.std"
        StandardFileWriter(results_file, df)()

        assert(res)


    def test_14(self):
        """Test #14 : Test le plugin avec l'option 'exact' égale à 16. Il doit retourné un message indiquant que le nombre exact est pas atteint!"""
        # open and read source
        source0 = plugin_test_dir + "input_big_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute CheckNumberOfLevels
        df = CheckNumberOfLevels(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT --pdsLabel G0928V4N] >> [CheckNumberOfLevels --exact 16]

        #write the result
        results_file = TMP_PATH + "test_14.std"
        StandardFileWriter(results_file, df)()

        assert(res)


    def test_15(self):
        """Test #15 : Test le plugin avec l'option 'allSame'. Il doit indiquer aucun message!"""
        # open and read source
        source0 = plugin_test_dir + "input_big_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute CheckNumberOfLevels
        df = CheckNumberOfLevels(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName VV,UU --pdsLabel R1558V0N] >> [CheckNumberOfLevels --allSame]

        #write the result
        results_file = TMP_PATH + "test_15.std"
        StandardFileWriter(results_file, df)()

        assert(res)


    def test_16(self):
        """Test #16 : Test le plugin avec l'option 'allSame'. Il doit retourné un message indiquant que les champs n'ont pas tous le mème nombre de niveau!"""
        # open and read source
        source0 = plugin_test_dir + "input_big_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute CheckNumberOfLevels
        df = CheckNumberOfLevels(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT --pdsLabel G0928V4N] >> [CheckNumberOfLevels --allSame]

        #write the result
        results_file = TMP_PATH + "test_16.std"
        StandardFileWriter(results_file, df)()

        assert(res)


    def test_17(self):
        """Test #17 : Test le plugin avec l'option 'allSame'. Test le cas où il y a deux types de grilles (2 gds différents) organisé de la façon suivante: gds1 : pds VV et UU qui ont le même nombre de niveaux soit 11 niveaux. gds2 : pds UU et VV qui ont le même nombre de niveaux soit 1 niveau. Il doit retourné un message indiquant que les champs n'ont pas tous le mème nombre de niveau!"""
        # open and read source
        source0 = plugin_test_dir + "input_big_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute CheckNumberOfLevels
        df = CheckNumberOfLevels(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName VV,UU --pdsLabel R1558V0N] >> [Select --fieldName UU,VV --pdsLabel G0928V4N] >> [CheckNumberOfLevels --allSame]

        #write the result
        results_file = TMP_PATH + "test_17.std"
        StandardFileWriter(results_file, df)()

        assert(res)


    def test_18(self):
        """Test #18 : Test le plugin avec l'option 'allSame'. Test le cas où il y a deux types de grilles (2 gds différents) organisé de la façon suivante: gds1 : pds VV et UU qui ont le même nombre de niveaux gds2 : pds TT(10 à 1000) et TT(12000) qui n'ont pas le même nombre de niveaux Il doit retourné un message indiquant que les champs n'ont pas tous le mème nombre de niveau!"""
        # open and read source
        source0 = plugin_test_dir + "input_big_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute CheckNumberOfLevels
        df = CheckNumberOfLevels(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName VV,UU --pdsLabel R1558V0N] >> [Select --fieldName TT --pdsLabel G0928V4N] >> [CheckNumberOfLevels --allSame]

        #write the result
        results_file = TMP_PATH + "test_18.std"
        StandardFileWriter(results_file, df)()

        assert(res)


    def test_19(self):
        """Test #19 : Test le plugin avec l'option 'allSameInGrids'. Il doit indiquer aucun message!"""
        # open and read source
        source0 = plugin_test_dir + "input_big_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute CheckNumberOfLevels
        df = CheckNumberOfLevels(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName VV,UU --pdsLabel R1558V0N] >> [CheckNumberOfLevels --allSameInGrids]

        #write the result
        results_file = TMP_PATH + "test_19.std"
        StandardFileWriter(results_file, df)()

        assert(res)


    def test_20(self):
        """Test #20 : Test le plugin avec l'option 'allSameInGrids'. Il doit retourné un message indiquant que les champs n'ont pas le même nombre de niveau sur la même grille!"""
        # open and read source
        source0 = plugin_test_dir + "input_big_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute CheckNumberOfLevels
        df = CheckNumberOfLevels(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT --pdsLabel G0928V4N] >> [CheckNumberOfLevels --allSameInGrids]

        #write the result
        results_file = TMP_PATH + "test_20.std"
        StandardFileWriter(results_file, df)()

        assert(res)


    def test_21(self):
        """Test #21 : Test le plugin avec l'option 'allSameInGrids'. Test le cas où il y a deux types de grilles (2 gds différents) organisé de la façon suivante: gds1 : pds VV et UU qui ont le même nombre de niveaux soit 11 niveaux. gds2 : pds UU et VV qui ont le même nombre de niveaux soit 1 niveau. Il doit retourné un message indiquant que les champs n'ont pas le même nombre de niveau sur la même grille!"""
        # open and read source
        source0 = plugin_test_dir + "input_big_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute CheckNumberOfLevels
        df = CheckNumberOfLevels(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName VV,UU --pdsLabel R1558V0N] >> [Select --fieldName UU,VV --pdsLabel G0928V4N] >> [CheckNumberOfLevels --allSameInGrids]

        #write the result
        results_file = TMP_PATH + "test_21.std"
        StandardFileWriter(results_file, df)()

        assert(res)


    def test_22(self):
        """Test #22 : Test le plugin avec l'option 'allSameInGrids'. Test le cas où il y a deux types de grilles (2 gds différents) organisé de la façon suivante: gds1 : pds VV et UU qui ont le même nombre de niveaux gds2 : pds TT(10 à 1000) et TT(12000) qui n'ont pas le même nombre de niveaux Il doit retourné un message indiquant que les champs n'ont pas le même nombre de niveau sur la même grille!"""
        # open and read source
        source0 = plugin_test_dir + "input_big_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute CheckNumberOfLevels
        df = CheckNumberOfLevels(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName VV,UU --pdsLabel R1558V0N] >> [Select --fieldName TT --pdsLabel G0928V4N] >> [CheckNumberOfLevels --allSameInGrids]

        #write the result
        results_file = TMP_PATH + "test_22.std"
        StandardFileWriter(results_file, df)()

        assert(res)
