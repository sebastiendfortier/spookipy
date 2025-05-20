import numpy as np
from typing import Dict, List, Tuple, Union, Optional
import rpnpy.librmn.all as rmn
import rpnpy.vgd.all as vgd
import rpnpy.librmn.proto as pt
from rpnpy.rpndate import RPNDate
import datetime


class RmnInterface:
    """Central interface for librmn/rpnpy functionality"""

    CONVIP_ENCODE = rmn.CONVIP_ENCODE
    CONVIP_ENCODE_OLD = rmn.CONVIP_ENCODE_OLD
    CONVIP_DECODE = rmn.CONVIP_DECODE

    LEVEL_KIND_PMB = rmn.LEVEL_KIND_PMB
    KIND_HOURS = rmn.KIND_HOURS

    TIME_KIND_HR = rmn.TIME_KIND_HR

    @staticmethod
    def find_records(
        file_id: int,
        nomvar: Optional[str] = None,
        ip1: Optional[int] = None,
        ip2: Optional[int] = None,
        datev: Optional[int] = None,
    ) -> List[Dict]:
        """Find records matching specified criteria

        Args:
            file_id: File ID from open_file
            nomvar: Variable name to search for
            ip1: IP1 value to match
            ip2: IP2 value to match
            datev: Valid date to match

        Returns:
            List of matching record metadata
        """
        kwargs = {}
        if nomvar is not None:
            kwargs["nomvar"] = nomvar
        if ip1 is not None:
            kwargs["ip1"] = ip1
        if ip2 is not None:
            kwargs["ip2"] = ip2
        if datev is not None:
            kwargs["datev"] = datev

        return list(rmn.fstinl(file_id, **kwargs))

    @staticmethod
    def read_record(record_key: int) -> Dict:
        """Read data from a record

        Args:
            file_id: File ID from open_file
            record_key: Record key from find_records, can be either the key dictionary or just the key integer

        Returns:
            Dictionary containing record data and metadata
        """
        return rmn.fstluk(record_key)

    @staticmethod
    def write_record(file_id: int, data: np.ndarray, record_meta: dict, rewrite: bool = False) -> None:
        """Write data to a record

        Args:
            file_id: File ID from open_file
            record_key: Record key from find_records
            data: Data to write
        """
        rmn.fstecr(file_id, data, record_meta, rewrite)

    @staticmethod
    def update_record_metadata(
        record_key: int,
        dateo: int,
        deet: int,
        npas: int,
        ni: int,
        nj: int,
        nk: int,
        datyp: int,
        ip1: int,
        ip2: int,
        ip3: int,
        typvar: str,
        nomvar: str,
        etiket: str,
        grtyp: str,
        ig1: int,
        ig2: int,
        ig3: int,
        ig4: int,
        keep_dateo: bool = False,
    ) -> None:
        """Update metadata for a record

        Args:
            file_id: File ID from open_file
            record_key: Record key from find_records
            record_meta: Metadata to update
        """
        rmn.fst_edit_dir(
            record_key,
            dateo,
            deet,
            npas,
            ni,
            nj,
            nk,
            datyp,
            ip1,
            ip2,
            ip3,
            typvar,
            nomvar,
            etiket,
            grtyp,
            ig1,
            ig2,
            ig3,
            ig4,
            keep_dateo,
        )

    @staticmethod
    def get_record_metadata(record_key: int) -> Dict:
        """Get metadata for a record

        Args:
            file_id: File ID from open_file
            record_key: Record metadata from find_records

        Returns:
            Dictionary containing record metadata
        """
        return rmn.fstprm(record_key)

    @staticmethod
    def create_grid_set(output_grid: int, input_grid: int) -> None:
        """Create a grid set by copying definitions from an input grid to an output grid.

        Args:
            input_grid: The input grid from which definitions are copied.
            output_grid: The output grid where definitions are defined.
        """
        rmn.ezdefset(output_grid, input_grid)

    @staticmethod
    def set_interpolation_values(option: str, value: float) -> None:
        """Set interpolation values

        Args:
            option: Option name
            value: Value to set
        """
        rmn.ezsetval(option, value)

    @staticmethod
    def get_interpolation_options(option: str, value: str):
        """Get interpolation values

        Args:
            option: Option name
        """
        return rmn.ezgetopt(option, value)

    @staticmethod
    def set_interpolation_options(option: str, value: str) -> None:
        """Set interpolation options

        Args:
            option: Option name
            value: Value to set
        """
        rmn.ezsetopt(option, value)

    @staticmethod
    def read_grid(file_id: int, record: Dict) -> int:
        """Read grid from a record

        Args:
            file_id: File ID from open_file
            record: Record from get_record_metadata

        Returns:
            Grid ID
        """
        return rmn.readGrid(file_id, record)

    @staticmethod
    def release_grid(grid_id: int) -> None:
        """Release a grid

        Args:
            grid_id: Grid ID from read_grid
        """
        rmn.gdrls(grid_id)

    @staticmethod
    def get_grid_parameters(grid_id: int) -> Dict:
        """Get grid parameters

        Args:
            grid_id: Grid ID from define_grid

        Returns:
            Dictionary containing grid parameters
        """
        return rmn.ezgxprm(grid_id)

    @staticmethod
    def define_grid_fmem(params: dict) -> Dict:
        """Define a new grid

        Args:
            params: Grid parameters

        Returns:
            Dictionary containing grid definition
        """
        return rmn.ezgdef_fmem(params)

    @staticmethod
    def define_grid(params: dict) -> Dict:
        """Define a new grid

        Args:
            params: Grid parameters

        Returns:
            Dictionary containing grid definition
        """
        return rmn.ezqkdef(params)

    @staticmethod
    def define_supergrid(params: dict) -> Dict:
        """Define a supergrid

        Args:
            params: Grid parameters

        Returns:
            Dictionary containing grid definition
        """
        return rmn.ezgdef_supergrid(**params)

    @staticmethod
    def calculate_distance_between_points(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate the distance between two points on the Earth's surface

        Args:
            lat1: Latitude of the first point
            lon1: Longitude of the first point
            lat2: Latitude of the second point
            lon2: Longitude of the second point

        Returns:
            Distance in kilometers
        """
        return rmn.ezcalcdist(lat1, lon1, lat2, lon2)

    @staticmethod
    def grid_definition_to_ig(grtyp, xg1, xg2, xg3, xg4) -> Tuple[int, int, int, int]:
        """Convert grid definition to ig values

        Args:
            sub_grid_ref: Subgrid reference
            encoded_igs: Encoded ig values

        Returns:
            Tuple of ig values
        """
        return rmn.cxgaig(grtyp, xg1, xg2, xg3, xg4)

    @staticmethod
    def get_lat_lon_from_grid(grid_id: int) -> Dict:
        """Get lat and lon from grid

        Args:
            grid_id: Grid ID from define_grid

        Returns:
            Dictionary containing lat and lon
        """
        return rmn.gdll(grid_id)

    @staticmethod
    def get_xy_from_lat_lon(grid_id: int, lat: List[float], lon: List[float]) -> Dict:
        """Get xy from lat and lon

        Args:
            grid_id: Grid ID from define_grid
            lat: Lat values
            lon: Lon values

        Returns:
            Dictionary containing xy
        """
        return rmn.gdxyfll(grid_id, lat, lon)

    @staticmethod
    def convert_grid_winds_at_grid_point(
        grid_id: int,
        uv: np.ndarray,
        wd: np.ndarray,
        uu: np.ndarray,
        vv: np.ndarray,
        lat: np.ndarray,
        lon: np.ndarray,
        lat_size: int,
    ) -> None:
        """Convert grid winds at grid point"""
        rmn.c_gdwdfuv(grid_id, uv, wd, uu, vv, lat, lon, lat_size)

    @staticmethod
    def scalar_interpolation(output_grid: int, input_grid: int, data: np.ndarray) -> np.ndarray:
        """Perform scalar interpolation on a DataFrame and handles extrapolation based on specified criteria."""
        return rmn.ezsint(output_grid, input_grid, data)

    @staticmethod
    def vectorial_interpolation(
        output_grid: int, input_grid: int, uu: np.ndarray, vv: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Perform vectorial interpolation on a DataFrame and handles extrapolation based on specified criteria."""
        return rmn.ezuvint(output_grid, input_grid, uu, vv)

    @staticmethod
    def encode_ip(rp1: rmn.FLOAT_IP, rp2: rmn.FLOAT_IP, rp3: rmn.FLOAT_IP) -> Tuple[float, int]:
        """Encode IP values

        Args:
            rp1: IP1 value
            rp2: IP2 value
            rp3: IP3 value

        Returns:
            Tuple of (value, kind)
        """
        return rmn.EncodeIp(rp1, rp2, rp3)

    @staticmethod
    def convert_ip(mode: int, ip: int, kind: int = 0):
        """Convert IP values

        Args:
            mode: Conversion mode (e.g., rmn.CONVIP_DECODE)
            ip1: IP1 value
            ip2: IP2 value
            ip3: IP3 value

        Returns:
            Tuple of (value, kind)
        """
        if mode in [rmn.CONVIP_ENCODE, rmn.CONVIP_ENCODE_OLD]:
            return rmn.convertIp(mode, float(ip), int(kind))
        else:
            return rmn.convertIp(mode, int(ip))

    @staticmethod
    def convert_to_float_ip(ip1: int, ip2: int, kind: int) -> rmn.FLOAT_IP:
        """Convert IP values to FLOAT_IP

        Args:
            ip1: IP1 value
            ip2: IP2 value
            kind: Kind value

        Returns:
            FLOAT_IP object
        """
        return rmn.FLOAT_IP(ip1, ip2, kind)

    @staticmethod
    def date_to_stamp(date: int, time: int = 0) -> int:
        """Convert date and time to timestamp

        Args:
            date: Date in YYYYMMDD format
            time: Time in HHMMSS format

        Returns:
            Timestamp value
        """
        return rmn.newdate(rmn.NEWDATE_PRINT2STAMP, date, time)

    @staticmethod
    def stamp_to_date(stamp: int) -> Tuple[int, int]:
        """Convert timestamp to date and time

        Args:
            stamp: Timestamp value

        Returns:
            Tuple of (date, time) in (YYYYMMDD, HHMMSS) format
        """
        return rmn.newdate(rmn.NEWDATE_STAMP2PRINT, stamp)

    @staticmethod
    def get_numpy_dtype(datyp: int, nbits: int) -> str:
        """
        Determines the numpy dtype based on the FST file's datyp and nbits.

        :param datyp: data type code from FST file
        :type datyp: int
        :param nbits: number of bits used for storage
        :type nbits: int
        :return: numpy dtype string
        :rtype: str
        """
        field_dtype = "float32"
        if (datyp in [1, 5, 6, 133, 134]) and (nbits <= 32):
            field_dtype = "float32"
        elif (datyp in [1, 5, 6, 133, 134]) and (nbits > 32):
            field_dtype = "float64"
        elif datyp in [2, 130]:
            field_dtype = "uint32"
        elif datyp in [4, 132]:
            if nbits > 1:
                field_dtype = "int32"
            elif nbits == 1:
                field_dtype = "uint32"
        return field_dtype

    @staticmethod
    def create_rpn_date(date: datetime.datetime, dt: int = 0, nstep: int = 0) -> int:
        """Create an RPN date from a datetime object."""
        return RPNDate(date, dt=dt, nstep=nstep)

    @staticmethod
    def decode_rpn_date(dateo: int) -> datetime.datetime:
        """Decode an RPN date to a datetime object."""
        return RPNDate(dateo).toDateTime()

    @staticmethod
    def kind_to_string(kind: int) -> str:
        """Convert a kind value to its string representation.

        Args:
            kind: The kind value to convert

        Returns:
            String representation of the kind, empty string for special values
        """
        return "" if kind in [-1, 3, 15, 17, 100] else rmn.kindToString(kind).strip()


class VGridInterface:
    """Interface for vertical grid operations"""

    @staticmethod
    def read_vgrid(file_id: int, ip1: int = -1, ip2: int = -1) -> "vgd.VGridDescriptor":
        """Read vertical grid descriptor

        Args:
            file_id: File ID from open_file
            ip1: IP1 value
            ip2: IP2 value

        Returns:
            Vertical grid descriptor
        """
        return vgd.vgd_read(file_id, ip1=ip1, ip2=ip2)

    @staticmethod
    def write_vgrid(vgrid: "vgd.VGridDescriptor", file_id: int) -> None:
        """Write vertical grid descriptor

        Args:
            vgrid: Vertical grid descriptor
            file_id: File ID from open_file
        """
        vgd.vgd_write(vgrid, file_id)

    @staticmethod
    def get_vgrid_param(vgrid: "vgd.VGridDescriptor", param: str) -> Union[int, float, np.ndarray]:
        """Get vertical grid parameter

        Args:
            vgrid: Vertical grid descriptor
            param: Parameter name to retrieve

        Returns:
            Parameter value
        """
        return vgd.vgd_get(vgrid, param)

    @staticmethod
    def new_pressure_vgrid(levels: List[float]) -> "vgd.VGridDescriptor":
        """Create new pressure-based vertical grid

        Args:
            levels: List of pressure levels

        Returns:
            New vertical grid descriptor
        """
        return vgd.vgd_new_pres(levels)
