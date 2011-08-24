%define modname xslcache
%define dirname %{modname}
%define soname %{modname}.so
%define inifile B06_%{modname}.ini

Summary:	A modified XSL extension that caches the parsed XSL stylesheet representation
Name:		php-%{modname}
Version:	0.7.1
Release:	%mkrel 11
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/xslcache/
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	libxml2-devel
BuildRequires:	libxslt-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The XSL Cache extension is a modification of PHP's standard XSL extension that
caches the parsed XSL stylesheet representation between sessions for 2.5x boost
in performance for sites that repeatedly apply the same transform. Although
there is still some further work that could be done on the extension, this code
is already proving beneficial in production use for a few applications on the
New York Times' website.

%prep

%setup -q -n %{modname}-%{version}
[ "../package*.xml" != "/" ] && mv ../package*.xml .

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}
%make
mv modules/*.so .

%install
rm -rf %{buildroot} 

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m755 %{soname} %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc CREDITS package*.xml 
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}

