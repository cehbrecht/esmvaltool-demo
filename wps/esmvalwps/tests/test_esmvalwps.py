from esmvalwps import esmvalwps


def test_generate_namelist():
    namelist = esmvalwps.generate_namelist(
        diag="overview",
        workspace="/tmp",
        start_year=2001,
        end_year=2005,
        output_format='ps')
    fp = open(namelist, 'r')
    content = fp.read()
    assert "ESGF_CMIP5 MPI-M output1 MPI-M MPI-ESM-LR historical mon atmos Amon r1i1p1 latest 1990 2000" in content
