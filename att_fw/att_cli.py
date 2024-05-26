from typing import Dict, Optional, List
from typing_extensions import Annotated

import typer

from att_fw.backend.att_cli_utils import CallBackFunctions
from att_fw.backend.att_prepare import ATT_Prepare
from att_fw import __att_version__


app = typer.Typer(no_args_is_help=True)


@app.command()
def run(
    campaign_name: Annotated[Optional[str], typer.Option('-c', '--campaign-name',
                                                         help="select test campaign to run",
                                                         callback=CallBackFunctions.campaign_name_callback)
                             ] = None,

    bench_config_name: Annotated[Optional[str],
                                 typer.Option('-b', '--bench-config',
                                              help="select test bench",
                                              callback=CallBackFunctions.bench_config_name_callback)
                                 ] = "default_bench_config",
    component_parameter: Annotated[Optional[List[str]],
                                   typer.Option("--ctp", "--component-parameters",
                                                help="to replace the existed components' parameter")
                                   ] = None,
    optional_parameter: Annotated[Optional[List[str]],
                                  typer.Option('--otp', '--optional-parameters',
                                               help="to replace the existed testlib configs' parameter")
                                  ] = None,
    campaign_id: Annotated[Optional[str],
                           typer.Option('--uuid',
                                        help='It specifies the generated UUID.')] = None,
    hot_boot: Annotated[Optional[bool],
                         typer.Option('--hot-boot',
                                      help="will load config from exist att cache db, if false: " +
                                      "will drop ALL config db and re-generate the config-db")] = False,
    rerun: Annotated[Optional[bool],
                     typer.Option('--rerun',
                                  help="rerun by uuid")] = False
):
    """
    该指令支持如下
        python3 ./att_fw/att_cli.py run -c test_login
    """
    component_parameter = CallBackFunctions.parse_extend_args_to_sql(component_parameter)
    optional_parameter = CallBackFunctions.parse_extend_args_to_sql(optional_parameter)
    ATT_Prepare()


@app.command()
def version():
    print(__att_version__)


if __name__ == "__main__":
    # typer.run(run_case)
    app()
