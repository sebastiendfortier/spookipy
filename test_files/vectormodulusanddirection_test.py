

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"VectorModulusAndDirection/testsFiles/"

class TestVectorModulusAndDirection(unittest.TestCase):

    def test_1(self):
        """Test #1 : Test l'option --orientationType avec la valeur WIND."""
        # open and read source
        source0 = plugin_test_dir + "inputInterpolatedToStation.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute VectorModulusAndDirection
        df = VectorModulusAndDirection(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [PrintIMO] >> [Select --fieldName UU,TT] >> [VectorModulusAndDirection --orientationType WIND] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "VectorModulusAndDirection_ygrid_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_2(self):
        """Test #2 : Test l'option --orientationType avec la valeur TRIG."""
        # open and read source
        source0 = plugin_test_dir + "inputInterpolatedToStation.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute VectorModulusAndDirection
        df = VectorModulusAndDirection(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName UU,TT] >> [VectorModulusAndDirection --orientationType TRIG] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "VectorModulusAndDirection_trig_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_3(self):
        """Test #3 : Test l'option --inputInterpolatedToStation avec une valeur autre que WIND et TRIG."""
        # open and read source
        source0 = plugin_test_dir + "inputInterpolatedToStation.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute VectorModulusAndDirection
        df = VectorModulusAndDirection(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [VectorModulusAndDirection --orientationType BLABLABLA] >> [WriterStd --output {destination_path}]

        #write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_4(self):
        """Test #4 : Test un fichier standard avec des champs sur une grille Y avec les tictic tactac définis sur une grille N."""
        # open and read source
        source0 = plugin_test_dir + "Ygrid_Ntypetictac_UUVV.fst"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute VectorModulusAndDirection
        df = VectorModulusAndDirection(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [VectorModulusAndDirection --orientationType WIND] >> [WriterStd --output {destination_path}]

        #write the result
        results_file = TMP_PATH + "test_4.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_5(self):
        """Test #5 : Test un fichier standard avec des champs sur une grille autre que celle autorisé."""
        # open and read source
        source0 = plugin_test_dir + "pm2001092012-01-00_000.fst"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute VectorModulusAndDirection
        df = VectorModulusAndDirection(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [VectorModulusAndDirection --orientationType WIND] >> [WriterStd --output {destination_path}]

        #write the result
        results_file = TMP_PATH + "test_5.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_6(self):
        """Test #6 : Test un fichier standard avec des champs sur une grille autre que celle autorisé."""
        # open and read source
        source0 = plugin_test_dir + "dm2001092012-00-00_000.fst"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute VectorModulusAndDirection
        df = VectorModulusAndDirection(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [VectorModulusAndDirection --orientationType WIND] >> [WriterStd --output {destination_path}]

        #write the result
        results_file = TMP_PATH + "test_6.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_7(self):
        """Test #7 : Test avec une grille U le calcul de la vitesse et de la direction des vents, référentiel météorologique."""
        # open and read source
        source0 = plugin_test_dir + "2015072100_240_TTESUUVV_YinYang.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute VectorModulusAndDirection
        df = VectorModulusAndDirection(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --fieldName UU,VV] >> [VectorModulusAndDirection --orientationType WIND] >> [WriterStd --output {destination_path}]

        #write the result
        results_file = TMP_PATH + "test_7.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "VecModAndDir_Ugrid_wind_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_8(self):
        """Test #8 : Test avec une grille U le calcul de la vitesse et de la direction des vents, référentiel trigonométrique."""
        # open and read source
        source0 = plugin_test_dir + "2015072100_240_TTESUUVV_YinYang.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute VectorModulusAndDirection
        df = VectorModulusAndDirection(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --fieldName UU,VV] >> [VectorModulusAndDirection --orientationType TRIG] >> [WriterStd --output {destination_path}]

        #write the result
        results_file = TMP_PATH + "test_8.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "VecModAndDir_Ugrid_trig_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


