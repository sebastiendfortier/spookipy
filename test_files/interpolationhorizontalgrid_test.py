

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"InterpolationHorizontalGrid/testsFiles/"

class TestInterpolationHorizontalGrid(unittest.TestCase):

    def test_regtest_1(self):
        """Test #1 :   Interpolation with multiple different input grid"""
        # open and read source
        source0 = plugin_test_dir + "input_big_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute InterpolationHorizontalGrid
        df = InterpolationHorizontalGrid(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [InterpolationHorizontalGrid -m USER_DEFINED --gridType TYPE_N --xyDimensions 191,141 -p 79.0,117.0,57150.0,21.0 --interpolationType BI-LINEAR --extrapolationType MAXIMUM] >> [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "interpolationHoriz_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_2(self):
        """Test #2 :   Interpolation with scalar fields only"""
        # open and read source
        source0 = plugin_test_dir + "4panneaux_input4_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute InterpolationHorizontalGrid
        df = InterpolationHorizontalGrid(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [InterpolationHorizontalGrid -m USER_DEFINED --gridType TYPE_N --xyDimensions 191,141 -p 79.0,117.0,57150.0,21.0 --interpolationType BI-LINEAR --extrapolationType MAXIMUM] >> [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "interpolationHorizScalar_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_3(self):
        """Test #3 :   Interpolation with vectorial fields only"""
        # open and read source
        source0 = plugin_test_dir + "inputUUVV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute InterpolationHorizontalGrid
        df = InterpolationHorizontalGrid(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [InterpolationHorizontalGrid -m USER_DEFINED --gridType TYPE_N --xyDimensions 191,141 -p 79.0,117.0,57150.0,21.0 --interpolationType BI-LINEAR --extrapolationType MAXIMUM] >> [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "interpolationHorizVectorial_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_5(self):
        """Test #5 :   Interpolation with FIELD_DEFINED"""
        # open and read source
        source0 = plugin_test_dir + "TTUUVVKTRT.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute InterpolationHorizontalGrid
        df = InterpolationHorizontalGrid(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [InterpolationHorizontalGrid -m FIELD_DEFINED --fieldName RT --interpolationType NEAREST --extrapolationType NEAREST] >> [WriterStd --output {destination_path} --makeIP1EncodingWorkWithTests]

        #write the result
        results_file = TMP_PATH + "test_5.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "fieldDefined_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_6(self):
        """Test #6 :   Interpolation with FIELD_DEFINED, make sure HY follow"""
        # open and read source
        source0 = plugin_test_dir + "TT_RT_reghyb"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute InterpolationHorizontalGrid
        df = InterpolationHorizontalGrid(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --fieldName TT,RT] >> [InterpolationHorizontalGrid -m FIELD_DEFINED --fieldName RT --interpolationType NEAREST --extrapolationType NEAREST] >> [WriterStd --output {destination_path} ]

        #write the result
        results_file = TMP_PATH + "test_6.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "fieldDefinedWithHY_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_7(self):
        """Test #7 :  Interpolation d'un champ scalaire (TT) d'une grille U vers une grille Z"""
        # open and read source
        source0 = plugin_test_dir + "2015072100_240_TTESUUVV_YinYang.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "2015072100_240_TTESUUVV_GridZ.std"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute InterpolationHorizontalGrid
        df = InterpolationHorizontalGrid(src_df0).compute()
        #([ReaderStd --input {sources[0]}] >> [Select --fieldName TT]) + ([ReaderStd --input {sources[1]}] >> [Select --fieldName ES]) >> [InterpolationHorizontalGrid -m FIELD_DEFINED --fieldName ES --interpolationType BI-CUBIC --extrapolationType NEAREST] >> [WriterStd --output {destination_path}]

        #write the result
        results_file = TMP_PATH + "test_7.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "InterpHorizGridUtoZ_rmn19_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_8(self):
        """Test #8 :  Interpolation d'un champ scalaire (TT) d'une grille Z vers une grille U"""
        # open and read source
        source0 = plugin_test_dir + "2015072100_240_TTESUUVV_YinYang.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "2015072100_240_TTESUUVV_GridZ.std"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute InterpolationHorizontalGrid
        df = InterpolationHorizontalGrid(src_df0).compute()
        #([ReaderStd --input {sources[0]}] >> [Select --fieldName ES]) + ([ReaderStd --input {sources[1]}] >> [Select --fieldName TT]) >> [InterpolationHorizontalGrid -m FIELD_DEFINED --fieldName ES --interpolationType BI-CUBIC --extrapolationType NEAREST] >> [WriterStd --output {destination_path} ]

        #write the result
        results_file = TMP_PATH + "test_8.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "InterpHorizGridZtoU_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_9(self):
        """Test #9 :  Interpolation de champs vectoriels (UU,VV) d'une grille U vers une grille Z"""
        # open and read source
        source0 = plugin_test_dir + "2015072100_240_TTESUUVV_YinYang.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "2015072100_240_TTESUUVV_GridZ.std"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute InterpolationHorizontalGrid
        df = InterpolationHorizontalGrid(src_df0).compute()
        #([ReaderStd --input {sources[0]}] >> [Select --fieldName UU,VV]) + ([ReaderStd --input {sources[1]}] >> [Select --fieldName TT]) >> [InterpolationHorizontalGrid -m FIELD_DEFINED --fieldName TT --interpolationType BI-CUBIC --extrapolationType NEAREST] >> [Select --fieldName UU,VV] >> [WriterStd --output {destination_path} ]

        #write the result
        results_file = TMP_PATH + "test_9.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "InterpHorizGridUtoZ_UUVV_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_10(self):
        """Test #10 :  Interpolation de champs vectoriels (UU,VV) d'une grille Z vers une grille U"""
        # open and read source
        source0 = plugin_test_dir + "2015072100_240_TTESUUVV_YinYang.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "2015072100_240_TTESUUVV_GridZ.std"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute InterpolationHorizontalGrid
        df = InterpolationHorizontalGrid(src_df0).compute()
        #([ReaderStd --input {sources[0]}] >> [Select --fieldName TT]) + ([ReaderStd --input {sources[1]}] >> [Select --fieldName UU,VV]) >> [InterpolationHorizontalGrid -m FIELD_DEFINED --fieldName TT --interpolationType BI-CUBIC --extrapolationType NEAREST] >> [Select --fieldName UU,VV] >> [WriterStd --output {destination_path} ]

        #write the result
        results_file = TMP_PATH + "test_10.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "InterpHorizGridZtoU_UUVV_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_11(self):
        """Test #11 :  Interpolation de champs vectoriels et scalaires d'une grille Z vers une grille U avec un fichier a interpoler contenant 2 toctocs."""
        # open and read source
        source0 = plugin_test_dir + "glbpres_TT_UU_VV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "2015072100_240_TTESUUVV_YinYang.std"
        src_df1 = fstpy.StandardFileReader(source1)

        source2 = plugin_test_dir + "2015072100_240_TTESUUVV_GridZ.std"
        src_df2 = fstpy.StandardFileReader(source2)


        #compute InterpolationHorizontalGrid
        df = InterpolationHorizontalGrid(src_df0).compute()
        #([ReaderStd --input {sources[0]}] >> [Select --fieldName TT,UU,VV]) + ([ReaderStd --input {sources[1]}] >> [Select --fieldName ES]) >> [InterpolationHorizontalGrid -m FIELD_DEFINED --fieldName ES --interpolationType BI-CUBIC --extrapolationType NEAREST] >> [WriterStd --output {destination_path} ]

        #write the result
        results_file = TMP_PATH + "test_11.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "InterpHorizGridUtoZ_manyToctocs_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_13(self):
        """Test #13 :   test extrapolation with negative value"""
        # open and read source
        source0 = plugin_test_dir + "TT_RT_reghyb"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute InterpolationHorizontalGrid
        df = InterpolationHorizontalGrid(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --fieldName TT] >> [InterpolationHorizontalGrid -m USER_DEFINED --gridType TYPE_N --xyDimensions 152,120 -p 52.0,120.0,50000.0,21.0 --interpolationType NEAREST --extrapolationType VALUE=-888.8] >> [WriterStd --output {destination_path} ]

        #write the result
        results_file = TMP_PATH + "test_13.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "extrapolationNegativeValue_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


