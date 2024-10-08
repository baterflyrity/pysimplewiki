from engine.converters import converter
from engine.path import Path

supported_extensions = """
arm
as
autoit
autohotkey
awk
mawk
nawk
gawk
bash
sh
zsh
basic
cs
c
h
cpp
hpp
cc
hh
cmake
css
cisco
clj
cson
curl
d
dart
dpr
dfm
pas
pascal
diff
patch
jinja
django
dns
zone
bind
dockerfile
docker
dos
bat
cmd
ebnf
elixir
elm
erl
fs
fix
flix
f90
f95
fortran
go
golang
gradle
graphql
xml
xhtml
rss
xsl
xsd
sjb
plist
http
https
hs
ini
toml
json
java
jsp
js
jsx
julia
kt
kotlin
tex
lisp
lua
makefile
mk
mak
make
mma
wl
matlab
mel
nim
nimrod
nsis
nginx
nginxconf
objectivec
mm
objc
php
perl
pl
pm
pgsql
ps
ps1
prolog
properties
py
pyw
gyp
profile
pycon
r
ruby
rb
gemspec
podspec
thor
irb
rust
rs
sas
scss
sql
scala
scheme
shell
console
sol
solidity
svelte
swift
tcl
tk
terraform
tf
hcl
tsql
ts
tsx
vbnet
vb
vba
vbs
vbscript
vhdl
verilog
v
vim
x86asm
yml
yaml
zs
"""


@converter(*[f'.{x.strip()}' for x in supported_extensions.split('\n') if x.strip()])
def load_sourcecode_file(path: Path) -> str:
	"""
	Convert different programming languages sources to HTML highlighted markup.
	"""
	sources = path.guess_text()
	if sources:
		return f'<pre><code class="language-{path.suffix.split(".")[-1]}">{sources.text}</code></pre>'
