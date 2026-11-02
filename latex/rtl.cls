% =====================================================================
%  rtl.cls — Template bersama "Lab Robotika Tanpa Lab"
%  Dipakai oleh semua dokumen: silabus, penawaran, proposal.
%
%  Pemakaian:
%    \documentclass{rtl}            % dokumen biasa (A4, 11pt)
%    \documentclass[onepage]{rtl}   % margin lebih rapat untuk one-pager
%
%  Metadata (sebelum \begin{document}):
%    \title{...} \subtitle{...} \doctype{...} \date{...}
%  Lalu panggil \makeheader di awal dokumen.
% =====================================================================
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{rtl}[2026/11/02 Lab Robotika Tanpa Lab]

\newif\if@onepage \@onepagefalse
\DeclareOption{onepage}{\@onepagetrue}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax
\LoadClass[a4paper,11pt]{article}

% ---------- Huruf & bahasa ----------
\RequirePackage[T1]{fontenc}
\RequirePackage[utf8]{inputenc}
\RequirePackage{lmodern}
\RequirePackage{microtype}
\renewcommand{\familydefault}{\sfdefault}

% Babel belum menyediakan bahasa Indonesia di semua distribusi TeX,
% jadi nama-nama standar diterjemahkan manual.
\renewcommand{\contentsname}{Daftar Isi}
\renewcommand{\tablename}{Tabel}
\renewcommand{\figurename}{Gambar}
\renewcommand{\refname}{Referensi}

% ---------- Tata letak ----------
\if@onepage
  \RequirePackage[margin=1.6cm,top=1.4cm,bottom=1.6cm]{geometry}
\else
  \RequirePackage[margin=2.2cm,top=2cm,bottom=2.4cm]{geometry}
\fi
\setlength{\parindent}{0pt}
\setlength{\parskip}{0.55em}
\linespread{1.08}

% ---------- Warna ----------
\RequirePackage{xcolor}
\definecolor{rtlnavy}{HTML}{14213D}
\definecolor{rtlteal}{HTML}{0F7C7A}
\definecolor{rtlamber}{HTML}{E09F3E}
\definecolor{rtlgray}{HTML}{5C6370}
\definecolor{rtllight}{HTML}{EEF5F5}

% ---------- Paket umum ----------
\RequirePackage{graphicx}
\RequirePackage{amssymb}
\RequirePackage{tabularx}
\RequirePackage{booktabs}
\RequirePackage{array}
\RequirePackage{multicol}
\raggedcolumns
\RequirePackage[shortlabels]{enumitem}
\setlist{itemsep=0.15em,topsep=0.3em,leftmargin=1.3em}
\setlist[itemize]{label={\color{rtlteal}\textbullet}}
\RequirePackage[most]{tcolorbox}
\RequirePackage{titlesec}
\RequirePackage{fancyhdr}
\RequirePackage{lastpage}
\RequirePackage[hidelinks]{hyperref}
\hypersetup{colorlinks=true,linkcolor=rtlteal,urlcolor=rtlteal}

% ---------- Judul bagian ----------
\titleformat{\section}{\Large\bfseries\color{rtlnavy}}{\thesection}{0.6em}{}[{\color{rtlteal}\titlerule[1.2pt]}]
\titleformat{\subsection}{\large\bfseries\color{rtlteal}}{\thesubsection}{0.5em}{}
\titleformat{\subsubsection}{\normalsize\bfseries\color{rtlnavy}}{}{0em}{}
\titlespacing*{\section}{0pt}{1.1em}{0.5em}
\titlespacing*{\subsection}{0pt}{0.9em}{0.3em}

% ---------- Metadata ----------
\newcommand{\@subtitle}{}
\newcommand{\subtitle}[1]{\renewcommand{\@subtitle}{#1}}
\newcommand{\@doctype}{Lab Robotika Tanpa Lab}
\newcommand{\doctype}[1]{\renewcommand{\@doctype}{#1}}
\newcommand{\brand}{Lab Robotika Tanpa Lab}
\newcommand{\contactline}{Muhammad Zacky Asy'ari \,·\, zacky.asyari1986@gmail.com \,·\, github.com/zacky131/robotika-tanpa-lab}

% ---------- Header & footer ----------
\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\fancyhead[L]{\small\color{rtlgray}\brand}
\fancyhead[R]{\small\color{rtlgray}\@doctype}
\fancyfoot[L]{\scriptsize\color{rtlgray}\contactline}
\fancyfoot[R]{\scriptsize\color{rtlgray}\thepage/\pageref*{LastPage}}
\fancypagestyle{plain}{\fancyhf{}\fancyfoot[L]{\scriptsize\color{rtlgray}\contactline}\fancyfoot[R]{\scriptsize\color{rtlgray}\thepage/\pageref*{LastPage}}}

% ---------- Blok judul ----------
\newcommand{\makeheader}{%
  \thispagestyle{plain}%
  \begin{tcolorbox}[enhanced,colback=rtlnavy,colframe=rtlnavy,arc=0pt,
      left=12pt,right=12pt,top=10pt,bottom=10pt,
      borderline west={5pt}{0pt}{rtlamber}]
    {\color{rtlamber}\small\bfseries\MakeUppercase{\@doctype}}\par\vspace{2pt}
    {\color{white}\LARGE\bfseries\@title}\par
    \ifx\@subtitle\empty\else\vspace{3pt}{\color{white!85!rtlnavy}\large\@subtitle}\par\fi
    \vspace{4pt}{\color{white!70!rtlnavy}\small\@date}
  \end{tcolorbox}\vspace{0.4em}}

% ---------- Kotak sorotan ----------
\newtcolorbox{sorotan}[1][]{enhanced,colback=rtllight,colframe=rtlteal,
  arc=2pt,boxrule=0.6pt,left=8pt,right=8pt,top=6pt,bottom=6pt,
  fonttitle=\bfseries,coltitle=white,colbacktitle=rtlteal,#1}
\newtcolorbox{catatan}[1][]{enhanced,colback=rtlamber!10,colframe=rtlamber,
  arc=2pt,boxrule=0.6pt,left=8pt,right=8pt,top=5pt,bottom=5pt,
  fonttitle=\bfseries,coltitle=rtlnavy,colbacktitle=rtlamber!60,#1}

% Kartu paket harga: \paket{Nama}{Harga}{isi}
\newcommand{\paket}[3]{%
  \begin{tcolorbox}[enhanced,colback=white,colframe=rtlteal,arc=3pt,boxrule=0.8pt,
      title={\bfseries #1},colbacktitle=rtlteal,coltitle=white,
      left=6pt,right=6pt,top=4pt,bottom=4pt,height fill=false]
    {\color{rtlnavy}\large\bfseries #2}\par\vspace{2pt}\small #3
  \end{tcolorbox}}

% Penanda untuk hal yang belum diputuskan (mudah dicari: grep TBD)
\newcommand{\tbd}[1]{\textcolor{rtlamber}{\bfseries[TBD: #1]}}

\endinput
