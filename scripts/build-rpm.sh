#!/bin/bash

NAME="comodit-client"
SPEC_FILE_NAME="comodit-client"
PLATFORMS=(epel-6-i386 epel-6-x86_64 epel-7-x86_64 fedora-22-x86_64 fedora-23-x86_64 fedora-24-x86_64)
TAR_CONTENT="comodit_client templates setup.py comodit auto_completion/comodit README.md doc/comodit.1 rpmbuild/etc"

# Create build structure
rpmdev-setuptree

cd `dirname $0`
cd ..

# Set version information
. scripts/build-pkg-functions
set_version $1 $2
generate_version_file $VERSION $RELEASE

tar -cvzf $HOME/rpmbuild/SOURCES/${NAME}-${VERSION}-${RELEASE}.tar.gz ${TAR_CONTENT}

sed "s/#VERSION#/${VERSION}/g" rpmbuild/SPECS/${SPEC_FILE_NAME}.spec.template > rpmbuild/SPECS/${SPEC_FILE_NAME}.spec
sed -i "s/#RELEASE#/${RELEASE}/g" rpmbuild/SPECS/${SPEC_FILE_NAME}.spec
sed -i "s/#COMMIT#/${COMMIT}/g" rpmbuild/SPECS/${SPEC_FILE_NAME}.spec

rpmbuild -ba rpmbuild/SPECS/${SPEC_FILE_NAME}.spec

if [ -f "/usr/bin/mock" ]
then
for platform in "${PLATFORMS[@]}"
do
    /usr/bin/mock -r ${platform} --rebuild $HOME/rpmbuild/SRPMS/${NAME}-${VERSION}-${RELEASE}*.src.rpm
    mkdir -p $HOME/packages/${platform}
    cp -f /var/lib/mock/${platform}/result/*.rpm $HOME/packages/${platform}
done
fi
