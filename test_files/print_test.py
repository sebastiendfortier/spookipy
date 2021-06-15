

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"Print/testsFiles/"

class TestPrint(unittest.TestCase):

    def test_regtest_2(self):
        """Test #2 : Imprime au format voir vers un fichier"""
        # open and read source
        source0 = plugin_test_dir + "UUVV10x10_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Print
        df = Print(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Print --voirIp1NewStyle --noHeader --voirLineCounterOff --outputType VOIR --output /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_2rFmuKC/test_2.txt]

        #write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        assert(res == False)


    def test_regtest_3(self):
        """Test #3 : Test voir avec un fichier qui possde un champ de type entier."""
        # open and read source
        source0 = plugin_test_dir + "regdiag_2012061300_012_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Print
        df = Print(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Print --noHeader --voirLineCounterOff --outputType VOIR --output /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_3CnlLaY/test_3.txt]

        #write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        assert(res == False)


    def test_regtest_5(self):
        """Test #5 : Test voir avec un petit fichier"""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Print
        df = Print(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Print --noHeader --voirLineCounterOff --outputType VOIR --output /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_5Z2LNjk/test_5.txt]

        #write the result
        results_file = TMP_PATH + "test_5.std"
        StandardFileWriter(results_file, df)()

        assert(res == False)


    def test_regtest_6(self):
        """Test #6 : Test voir avec un gros fichier"""
        # open and read source
        source0 = plugin_test_dir + "input_big_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Print
        df = Print(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Print --noHeader --voirLineCounterOff --outputType VOIR --output /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_64RSYBG/test_6.txt]

        #write the result
        results_file = TMP_PATH + "test_6.std"
        StandardFileWriter(results_file, df)()

        assert(res == False)


    def test_regtest_7(self):
        """Test #7 : test_voir_print_sigma12000_pressure"""
        # open and read source
        source0 = plugin_test_dir + "input_model"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Print
        df = Print(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Print --noHeader --voirLineCounterOff --outputType VOIR --output /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_7RRyoo3/test_7.txt]

        #write the result
        results_file = TMP_PATH + "test_7.std"
        StandardFileWriter(results_file, df)()

        assert(res == False)


    def test_regtest_8(self):
        """Test #8 : test_voir_print_file_with_duplicated_grid"""
        # open and read source
        source0 = plugin_test_dir + "fstdWithDuplicatedGrid_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Print
        df = Print(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Print --noHeader --voirLineCounterOff --outputType VOIR --output /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_8Y39dIr/test_8.txt]

        #write the result
        results_file = TMP_PATH + "test_8.std"
        StandardFileWriter(results_file, df)()

        assert(res == False)


    def test_regtest_9(self):
        """Test #9 : test_voir_print_64bit"""
        # open and read source
        source0 = plugin_test_dir + "tt_stg_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Print
        df = Print(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Print --noHeader --voirLineCounterOff --outputType VOIR --output /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_9LU4YkQ/test_9.txt]

        #write the result
        results_file = TMP_PATH + "test_9.std"
        StandardFileWriter(results_file, df)()

        assert(res == False)


    def test_regtest_10(self):
        """Test #10 : test_voir_print_3_file"""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "windChill_file2cmp.std"
        src_df1 = fstpy.StandardFileReader(source1)

        source2 = plugin_test_dir + "windModulus_file2cmp.std"
        src_df2 = fstpy.StandardFileReader(source2)


        #compute Print
        df = Print(src_df0).compute()
        #[ReaderStd --input {sources[0]} {sources[1]} {sources[2]}] >> [Print --voirIp1NewStyle --noHeader --voirLineCounterOff --outputType VOIR --output /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_10ceDjDf/test_10.txt]

        #write the result
        results_file = TMP_PATH + "test_10.std"
        StandardFileWriter(results_file, df)()

        assert(res == False)


    def test_regtest_11(self):
        """Test #11 : test_voir_print_ip3"""
        # open and read source
        source0 = plugin_test_dir + "ip3.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Print
        df = Print(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Print --noHeader --voirLineCounterOff --outputType VOIR --output /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_11j0335E/test_11.txt]

        #write the result
        results_file = TMP_PATH + "test_11.std"
        StandardFileWriter(results_file, df)()

        assert(res == False)


    def test_regtest_12(self):
        """Test #12 : test_voir_print_ip1_mb_newstyle"""
        # open and read source
        source0 = plugin_test_dir + "UUVV93423264_hyb_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Print
        df = Print(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Print --voirIp1NewStyle --noHeader --voirLineCounterOff --outputType VOIR --output /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_12AmV5H4/test_12.txt]

        #write the result
        results_file = TMP_PATH + "test_12.std"
        StandardFileWriter(results_file, df)()

        assert(res == False)


    def test_regtest_13(self):
        """Test #13 : test voir print fields with typvar == PZ"""
        # open and read source
        source0 = plugin_test_dir + "UUVVTT5x5x2_fileSrc_PZ.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Print
        df = Print(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Print --noHeader --voirLineCounterOff --outputType VOIR --output /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_13lYpeyu/test_13.txt]

        #write the result
        results_file = TMP_PATH + "test_13.std"
        StandardFileWriter(results_file, df)()

        assert(res == False)


    def test_regtest_14(self):
        """Test #14 : test voir print fields with typvar == PU"""
        # open and read source
        source0 = plugin_test_dir + "UUVVTT5x5x2_fileSrc_PU.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Print
        df = Print(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Print --noHeader --voirLineCounterOff --outputType VOIR --output /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_14CUXVxU/test_14.txt]

        #write the result
        results_file = TMP_PATH + "test_14.std"
        StandardFileWriter(results_file, df)()

        assert(res == False)


    def test_regtest_15(self):
        """Test #15 : test voir print fields with typvar == PI"""
        # open and read source
        source0 = plugin_test_dir + "UUVVTT5x5x2_fileSrc_PI.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Print
        df = Print(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Print --noHeader --voirLineCounterOff --outputType VOIR --output /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_15xvtYGk/test_15.txt]

        #write the result
        results_file = TMP_PATH + "test_15.std"
        StandardFileWriter(results_file, df)()

        assert(res == False)


    def test_regtest_16(self):
        """Test #16 : test voir print fields with typvar == PF"""
        # open and read source
        source0 = plugin_test_dir + "UUVVTT5x5x2_fileSrc_PF.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Print
        df = Print(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Print --noHeader --voirLineCounterOff --outputType VOIR --output /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_16UB3mZK/test_16.txt]

        #write the result
        results_file = TMP_PATH + "test_16.std"
        StandardFileWriter(results_file, df)()

        assert(res == False)


    def test_regtest_17(self):
        """Test #17 : test voir print fields with typvar == PM"""
        # open and read source
        source0 = plugin_test_dir + "UUVVTT5x5x2_fileSrc_PM.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Print
        df = Print(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Print --noHeader --voirLineCounterOff --outputType VOIR --output /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_17fMnkrb/test_17.txt]

        #write the result
        results_file = TMP_PATH + "test_17.std"
        StandardFileWriter(results_file, df)()

        assert(res == False)


    def test_regtest_18(self):
        """Test #18 : test voir if HY is put in memory and print back when we have a grid with two kind of level, one of them being hybrid"""
        # open and read source
        source0 = plugin_test_dir + "mb_plus_hybrid_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Print
        df = Print(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Print --noHeader --voirLineCounterOff --outputType VOIR --output /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_180vRr2B/test_18.txt]

        #write the result
        results_file = TMP_PATH + "test_18.std"
        StandardFileWriter(results_file, df)()

        assert(res == False)


    def test_regtest_19(self):
        """Test #19 : test voir that PT is NOT read by the reader when the level type of the fields on the grid is not sigma"""
        # open and read source
        source0 = plugin_test_dir + "pt_with_hybrid.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Print
        df = Print(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Print --noHeader --voirLineCounterOff --outputType VOIR --output /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_193Nyyo3/test_19.txt]

        #write the result
        results_file = TMP_PATH + "test_19.std"
        StandardFileWriter(results_file, df)()

        assert(res == False)


    def test_regtest_20(self):
        """Test #20 : test voir that PT is NOT printed back when there is a PT field created in memory and the level type of the fields on the grid is not sigma"""
        # open and read source
        source0 = plugin_test_dir + "kt_ai_hybrid.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Print
        df = Print(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Print --noHeader --voirLineCounterOff --outputType VOIR --output /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_20Majpjv/test_20.txt]

        #write the result
        results_file = TMP_PATH + "test_20.std"
        StandardFileWriter(results_file, df)()

        assert(res == False)


    def test_regtest_21(self):
        """Test #21 : Test voir print ip2 != deet * npas"""
        # open and read source
        source0 = plugin_test_dir + "2012121000_cancm3_m1_00_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Print
        df = Print(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Print --voirIp1NewStyle --noHeader --voirLineCounterOff --outputType VOIR --output /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_21fUF4MX/test_21.txt]

        #write the result
        results_file = TMP_PATH + "test_21.std"
        StandardFileWriter(results_file, df)()

        assert(res == False)


    def test_regtest_22(self):
        """Test #22 : Test voir print of a pilot file"""
        # open and read source
        source0 = plugin_test_dir + "2015040800_030_piloteta"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Print
        df = Print(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Print --voirIp1NewStyle --noHeader --voirLineCounterOff --outputType VOIR --output /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_22ApSqKq/test_22.txt]

        #write the result
        results_file = TMP_PATH + "test_22.std"
        StandardFileWriter(results_file, df)()

        assert(res == False)


    def test_regtest_23(self):
        """Test #23 : test voir print file glbpres"""
        # open and read source
        source0 = plugin_test_dir + "glbpres_TT_UU_VV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Print
        df = Print(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Print --voirIp1NewStyle --noHeader --voirLineCounterOff --outputType VOIR --output /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_235fnb3U/test_23.txt]

        #write the result
        results_file = TMP_PATH + "test_23.std"
        StandardFileWriter(results_file, df)()

        assert(res == False)


    def test_regtest_24(self):
        """Test #24 : test voir print of files containing special chars and of multiple input files"""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5_+fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "wind+Chill_file2cmp.std"
        src_df1 = fstpy.StandardFileReader(source1)

        source2 = plugin_test_dir + "windModulus_file2cmp.std"
        src_df2 = fstpy.StandardFileReader(source2)


        #compute Print
        df = Print(src_df0).compute()
        #[ReaderStd --input {sources[0]} {sources[1]} {sources[2]}] >> [Print --voirIp1NewStyle --noHeader --voirLineCounterOff --outputType VOIR --output /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_24Ous0Yp/test_24.txt]

        #write the result
        results_file = TMP_PATH + "test_24.std"
        StandardFileWriter(results_file, df)()

        assert(res == False)


    def test_regtest_25(self):
        """Test #25 : test print fststat"""
        # open and read source
        source0 = plugin_test_dir + "UUVV10x10_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Print
        df = Print(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Print --noHeader --outputType FSTSTAT --output /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_25FXna5U/test_25.txt]

        #write the result
        results_file = TMP_PATH + "test_25.std"
        StandardFileWriter(results_file, df)()

        assert(res == False)


    def test_regtest_26(self):
        """Test #26 : Test fststat avec un fichier qui possde un champ de type entier."""
        # open and read source
        source0 = plugin_test_dir + "regdiag_2012061300_012_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Print
        df = Print(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Print --noHeader --outputType FSTSTAT --output /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_26aEylvq/test_26.txt]

        #write the result
        results_file = TMP_PATH + "test_26.std"
        StandardFileWriter(results_file, df)()

        assert(res == False)


    def test_regtest_27(self):
        """Test #27 : Test fststat avec un petit fichier"""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Print
        df = Print(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Print --noHeader --outputType FSTSTAT --output /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_27LkalRY/test_27.txt]

        #write the result
        results_file = TMP_PATH + "test_27.std"
        StandardFileWriter(results_file, df)()

        assert(res == False)


    def test_regtest_28(self):
        """Test #28 : Test fststat avec un gros fichier"""
        # open and read source
        source0 = plugin_test_dir + "input_big_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Print
        df = Print(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Print --noHeader --outputType FSTSTAT --output /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_28WpMdox/test_28.txt]

        #write the result
        results_file = TMP_PATH + "test_28.std"
        StandardFileWriter(results_file, df)()

        assert(res == False)


    def test_regtest_29(self):
        """Test #29 : test_fststat_print_sigma12000_pressure"""
        # open and read source
        source0 = plugin_test_dir + "input_model"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Print
        df = Print(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Print --noHeader --outputType FSTSTAT --output /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_29hS1Sob/test_29.txt]

        #write the result
        results_file = TMP_PATH + "test_29.std"
        StandardFileWriter(results_file, df)()

        assert(res == False)


    def test_regtest_30(self):
        """Test #30 : test_fststat_print_file_with_duplicated_grid"""
        # open and read source
        source0 = plugin_test_dir + "fstdWithDuplicatedGrid_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Print
        df = Print(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Print --noHeader --outputType FSTSTAT --output /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_30Qxlvr4/test_30.txt]

        #write the result
        results_file = TMP_PATH + "test_30.std"
        StandardFileWriter(results_file, df)()

        assert(res == False)


    def test_regtest_31(self):
        """Test #31 : test_fststat_print_64bit"""
        # open and read source
        source0 = plugin_test_dir + "tt_stg_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Print
        df = Print(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Print --noHeader --outputType FSTSTAT --output /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_31x5hKhY/test_31.txt]

        #write the result
        results_file = TMP_PATH + "test_31.std"
        StandardFileWriter(results_file, df)()

        assert(res == False)


    def test_regtest_32(self):
        """Test #32 : test_fststat_print_3_file"""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "windChill_file2cmp.std"
        src_df1 = fstpy.StandardFileReader(source1)

        source2 = plugin_test_dir + "windModulus_file2cmp.std"
        src_df2 = fstpy.StandardFileReader(source2)


        #compute Print
        df = Print(src_df0).compute()
        #[ReaderStd --input {sources[0]} {sources[1]} {sources[2]}] >> [Print --noHeader --outputType FSTSTAT --output /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_328EQ6TX/test_32.txt]

        #write the result
        results_file = TMP_PATH + "test_32.std"
        StandardFileWriter(results_file, df)()

        assert(res == False)


    def test_regtest_33(self):
        """Test #33 : test_fststat_print_ip3"""
        # open and read source
        source0 = plugin_test_dir + "ip3.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Print
        df = Print(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Print --noHeader --outputType FSTSTAT --output /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_33lbusIX/test_33.txt]

        #write the result
        results_file = TMP_PATH + "test_33.std"
        StandardFileWriter(results_file, df)()

        assert(res == False)


    def test_regtest_34(self):
        """Test #34 : test_fststat_print_ip1_mb_newstyle"""
        # open and read source
        source0 = plugin_test_dir + "UUVV93423264_hyb_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Print
        df = Print(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Print --noHeader --outputType FSTSTAT --output /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_348LVPHX/test_34.txt]

        #write the result
        results_file = TMP_PATH + "test_34.std"
        StandardFileWriter(results_file, df)()

        assert(res == False)


    def test_regtest_35(self):
        """Test #35 : test fststat print fields with typvar == PZ"""
        # open and read source
        source0 = plugin_test_dir + "UUVVTT5x5x2_fileSrc_PZ.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Print
        df = Print(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Print --noHeader --outputType FSTSTAT --output /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_357PNFjY/test_35.txt]

        #write the result
        results_file = TMP_PATH + "test_35.std"
        StandardFileWriter(results_file, df)()

        assert(res == False)


    def test_regtest_36(self):
        """Test #36 : test fststat print fields with typvar == PU"""
        # open and read source
        source0 = plugin_test_dir + "UUVVTT5x5x2_fileSrc_PU.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Print
        df = Print(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Print --noHeader --outputType FSTSTAT --output /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_36CTcO6Y/test_36.txt]

        #write the result
        results_file = TMP_PATH + "test_36.std"
        StandardFileWriter(results_file, df)()

        assert(res == False)


    def test_regtest_37(self):
        """Test #37 : test fststat print fields with typvar == PI"""
        # open and read source
        source0 = plugin_test_dir + "UUVVTT5x5x2_fileSrc_PI.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Print
        df = Print(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Print --noHeader --outputType FSTSTAT --output /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_37T7sw4Z/test_37.txt]

        #write the result
        results_file = TMP_PATH + "test_37.std"
        StandardFileWriter(results_file, df)()

        assert(res == False)


    def test_regtest_38(self):
        """Test #38 : test fststat print fields with typvar == PF"""
        # open and read source
        source0 = plugin_test_dir + "UUVVTT5x5x2_fileSrc_PF.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Print
        df = Print(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Print --noHeader --outputType FSTSTAT --output /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_38GRKid1/test_38.txt]

        #write the result
        results_file = TMP_PATH + "test_38.std"
        StandardFileWriter(results_file, df)()

        assert(res == False)


    def test_regtest_39(self):
        """Test #39 : test fststat print fields with typvar == PM"""
        # open and read source
        source0 = plugin_test_dir + "UUVVTT5x5x2_fileSrc_PM.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Print
        df = Print(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Print --noHeader --outputType FSTSTAT --output /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_393xoTw2/test_39.txt]

        #write the result
        results_file = TMP_PATH + "test_39.std"
        StandardFileWriter(results_file, df)()

        assert(res == False)


    def test_regtest_40(self):
        """Test #40 : test fststat if HY is put in memory and print back when we have a grid with two kind of level, one of them being hybrid"""
        # open and read source
        source0 = plugin_test_dir + "mb_plus_hybrid_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Print
        df = Print(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Print --noHeader --outputType FSTSTAT --output /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_406UCy13/test_40.txt]

        #write the result
        results_file = TMP_PATH + "test_40.std"
        StandardFileWriter(results_file, df)()

        assert(res == False)


    def test_regtest_41(self):
        """Test #41 : test fststat that PT is NOT read by the reader when the level type of the fields on the grid is not sigma"""
        # open and read source
        source0 = plugin_test_dir + "pt_with_hybrid.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Print
        df = Print(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Print --noHeader --outputType FSTSTAT --output /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_41tehh9a/test_41.txt]

        #write the result
        results_file = TMP_PATH + "test_41.std"
        StandardFileWriter(results_file, df)()

        assert(res == False)


    def test_regtest_42(self):
        """Test #42 : test fststat that PT is NOT printed back when there is a PT field created in memory and the level type of the fields on the grid is not sigma"""
        # open and read source
        source0 = plugin_test_dir + "kt_ai_hybrid.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Print
        df = Print(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Print --noHeader --outputType FSTSTAT --output /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_4222N0jn/test_42.txt]

        #write the result
        results_file = TMP_PATH + "test_42.std"
        StandardFileWriter(results_file, df)()

        assert(res == False)


    def test_regtest_43(self):
        """Test #43 : Test fststat print ip2 != deet * npas"""
        # open and read source
        source0 = plugin_test_dir + "2012121000_cancm3_m1_00_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Print
        df = Print(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Print --noHeader --outputType FSTSTAT --output /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_43DvjcEE/test_43.txt]

        #write the result
        results_file = TMP_PATH + "test_43.std"
        StandardFileWriter(results_file, df)()

        assert(res == False)


    def test_regtest_44(self):
        """Test #44 : Test fststat print of a plot file"""
        # open and read source
        source0 = plugin_test_dir + "2015040800_030_piloteta"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Print
        df = Print(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Print --noHeader --outputType FSTSTAT --output /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_44s95BkW/test_44.txt]

        #write the result
        results_file = TMP_PATH + "test_44.std"
        StandardFileWriter(results_file, df)()

        assert(res == False)


    def test_regtest_45(self):
        """Test #45 : test fststat print file glbpres"""
        # open and read source
        source0 = plugin_test_dir + "glbpres_TT_UU_VV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Print
        df = Print(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Print --noHeader --outputType FSTSTAT --output /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_457XGv4l/test_45.txt]

        #write the result
        results_file = TMP_PATH + "test_45.std"
        StandardFileWriter(results_file, df)()

        assert(res == False)


    def test_regtest_46(self):
        """Test #46 : test fststat print of files containing special chars and of multiple input files"""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5_+fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "wind+Chill_file2cmp.std"
        src_df1 = fstpy.StandardFileReader(source1)

        source2 = plugin_test_dir + "windModulus_file2cmp.std"
        src_df2 = fstpy.StandardFileReader(source2)


        #compute Print
        df = Print(src_df0).compute()
        #[ReaderStd --input {sources[0]} {sources[1]} {sources[2]}] >> [Print --noHeader --outputType FSTSTAT --output /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_46G1zaiY/test_46.txt]

        #write the result
        results_file = TMP_PATH + "test_46.std"
        StandardFileWriter(results_file, df)()

        assert(res == False)


