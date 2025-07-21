from pathlib import Path
from pysmi.reader.localfile import FileReader
from pysmi.writer.localfile import FileWriter
from pysmi.parser.smi import SmiV2Parser
from pysmi.codegen.pysnmp import PySnmpCodeGen
from pysmi.compiler import MibCompiler

# Optional: Enable debugging output
# from pysmi import debug
# debug.set_logger(debug.Debug('all'))

def compile_mib(mib_names, mib_source_dir, output_dir):
    # pathlibでディレクトリ作成
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    reader = FileReader(mib_source_dir)
    writer = FileWriter(output_dir)
    writer.suffix = '.py'  # Ensure the output files have .py extension
    parser = SmiV2Parser()
    code_generator = PySnmpCodeGen()
    compiler = MibCompiler(parser, code_generator, writer)
    compiler.add_sources(reader)
    results = compiler.compile(*mib_names)
    print(results)


if __name__ == "__main__":
    compile_mib(
        mib_names=('SNMPv2-CONF', 'SNMPv2-SMI', 'SNMPv2-TC', 'ARBORNET-PEAKFLOW-SP-MIB'),
        mib_source_dir='./mibs',
        output_dir='./compiled_mibs'
    )
