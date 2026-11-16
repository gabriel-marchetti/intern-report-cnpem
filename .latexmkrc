# fontspec exige LuaLaTeX ou XeLaTeX.
$pdf_mode = 4;
$lualatex = 'lualatex -shell-escape -interaction=nonstopmode -halt-on-error %O %S';

# Mantém o cache de fontes em um diretório gravável do projeto.
use Cwd qw(abs_path);
use File::Path qw(make_path);
my $cache = abs_path('.') . '/.cache/texmf';
make_path($cache);
$ENV{'TEXMFVAR'} = $cache;
