

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"LiftedIndex/testsFiles/"

class TestLiftedIndex(unittest.TestCase):

    def test_1(self):
        """Test #1 : Tester l'option --liftedFrom avec une valeur invalide."""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute LiftedIndex
        df = LiftedIndex(src_df0).compute()
        #[LiftedIndex --liftedFrom LIFTED_SOMEHOW]

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_2(self):
        """Test #2 : Tester l'option --increment avec une valeur invalide."""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute LiftedIndex
        df = LiftedIndex(src_df0).compute()
        #[LiftedIndex --liftedFrom SURFACE --increment 0.0mb]

        #write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_3(self):
        """Test #3 : Tester l'option --referenceLevel avec une valeur invalide."""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute LiftedIndex
        df = LiftedIndex(src_df0).compute()
        #[LiftedIndex --liftedFrom SURFACE --referenceLevel 0.0sg]

        #write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_4(self):
        """Test #4 : Tester l'option --liftedFrom MEAN_LAYER sans --baseMeanLayer ni --deltaMeanLayer."""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute LiftedIndex
        df = LiftedIndex(src_df0).compute()
        #[LiftedIndex --liftedFrom MEAN_LAYER]

        #write the result
        results_file = TMP_PATH + "test_4.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_5(self):
        """Test #5 : Tester l'option --liftedFrom MEAN_LAYER sans --deltaMeanLayer."""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute LiftedIndex
        df = LiftedIndex(src_df0).compute()
        #[LiftedIndex --liftedFrom MEAN_LAYER --baseMeanLayer SURFACE]

        #write the result
        results_file = TMP_PATH + "test_5.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_6(self):
        """Test #6 : Tester l'option --deltaMostUnstable avec une valeur invalide."""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute LiftedIndex
        df = LiftedIndex(src_df0).compute()
        #[LiftedIndex --liftedFrom MOST_UNSTABLE --deltaMostUnstable 0.0sg]

        #write the result
        results_file = TMP_PATH + "test_6.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_7(self):
        """Test #7 :  Calcul de l'indice de soulèvement à partir d'un fichier pression et du niveau de surface d'un fichier hybrid."""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_regpres"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute LiftedIndex
        df = LiftedIndex(src_df0).compute()
        #([ReaderStd --input {sources[0]}] + ([ReaderStd --input /home/spst900/spooki/spooki_dir_ppp4/pluginsRelatedStuff/LiftedIndex/testsFiles/2011100712_012_reghyb] >> [Select --verticalLevel SURFACE])) >> [LiftedIndex --liftedFrom SURFACE,SHOWALTER] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_7.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2011100712_012_regpres_Surface_Showalter_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_8(self):
        """Test #8 :  Calcul de l'indice de soulèvement à partir d'un fichier pression (SHOWALTER)."""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_regpres"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute LiftedIndex
        df = LiftedIndex(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [LiftedIndex --liftedFrom SHOWALTER] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_8.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2011100712_012_regpres_Showalter_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_9(self):
        """Test #9 :  Calcul de l'indice de soulèvement à partir d'un fichier hybrid et pression (MEAN_LAYER)."""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_reghyb"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute LiftedIndex
        df = LiftedIndex(src_df0).compute()
        #[ReaderStd --input {sources[0]} /home/spst900/spooki/spooki_dir_ppp4/pluginsRelatedStuff/LiftedIndex/testsFiles/2011100712_012_regpres] >> [LiftedIndex --liftedFrom MEAN_LAYER --baseMeanLayer SURFACE --deltaMeanLayer 100mb] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_9.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2011100712_012_reghyb_MeanLayer_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_10(self):
        """Test #10 :  Calcul de l'indice de soulèvement à partir d'un fichier hybrid et pression (MOST_UNSTABLE)."""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_reghyb"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute LiftedIndex
        df = LiftedIndex(src_df0).compute()
        #[ReaderStd --input {sources[0]} /home/spst900/spooki/spooki_dir_ppp4/pluginsRelatedStuff/LiftedIndex/testsFiles/2011100712_012_regpres] >> [LiftedIndex --liftedFrom MOST_UNSTABLE --deltaMostUnstable 300mb] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_10.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2011100712_012_reghyb_MostUnstable_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)
