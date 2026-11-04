#!/bin/bash
set -euo pipefail
W=/work
B=/work/work/cache   # on the Windows drive: downloads and the result
C=/cache              # docker volume (case-sensitive): the unpacked NDK
mkdir -p $B/cpm $B/dist $B/dl $C
export DEBIAN_FRONTEND=noninteractive
if ! command -v ninja >/dev/null; then
  apt-get update -qq
  apt-get install -y -qq g++ cmake ninja-build git curl unzip ca-certificates python3 >/dev/null
fi
# --- dependency cache (the layout native/modules/CMakeLists.txt expects)
[ -d $B/cpm/fmt/12.1.0/include ] || { git clone -q --depth 1 --branch 12.1.0 https://github.com/fmtlib/fmt.git $B/dl/fmt; mkdir -p $B/cpm/fmt/12.1.0; cp -r $B/dl/fmt/include $B/cpm/fmt/12.1.0/include; }
[ -d $B/cpm/nlohmann_json/v3.12.0/include ] || { git clone -q --depth 1 --branch v3.12.0 https://github.com/nlohmann/json.git $B/dl/json; mkdir -p $B/cpm/nlohmann_json/v3.12.0; cp -r $B/dl/json/include $B/cpm/nlohmann_json/v3.12.0/include; }
[ -d $B/cpm/zstd/1.5.7/lib ] || { git clone -q --depth 1 --branch v1.5.7 https://github.com/facebook/zstd.git $B/dl/zstd; mkdir -p $B/cpm/zstd/1.5.7; cp -r $B/dl/zstd/lib $B/cpm/zstd/1.5.7/lib; }
[ -d $B/cpm/lz4/1.10.0/lib ] || { git clone -q --depth 1 --branch v1.10.0 https://github.com/lz4/lz4.git $B/dl/lz4; mkdir -p $B/cpm/lz4/1.10.0; cp -r $B/dl/lz4/lib $B/cpm/lz4/1.10.0/lib; }
# --- NDK r28c (28.2.13676358)
if [ ! -d $C/android-ndk-r28c ]; then
  [ -s $B/dl/ndk.zip ] || curl -sSL -o $B/dl/ndk.zip https://dl.google.com/android/repository/android-ndk-r28c-linux.zip
  unzip -q -o $B/dl/ndk.zip -d $C
fi
NDK=$C/android-ndk-r28c
COMMON="-DEDEN_SOURCE_ROOT=$W/eden-duo-src -DEDEN_CPM_CACHE=$B/cpm -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTING=OFF"
echo "== linux"
cmake -S $W/companions/native/modules -B /tmp/build-linux -G Ninja $COMMON
cmake --build /tmp/build-linux --parallel 16 --target dsmod-fe3h
echo "== android"
cmake -S $W/companions/native/modules -B /tmp/build-android -G Ninja $COMMON \
  -DCMAKE_TOOLCHAIN_FILE=$NDK/build/cmake/android.toolchain.cmake -DANDROID_ABI=arm64-v8a \
  -DANDROID_PLATFORM=android-24 -DANDROID_STL=c++_static -DEDEN_ACNH_BUILD_DIAGNOSTICS=OFF
cmake --build /tmp/build-android --parallel 16 --target dsmod-fe3h
mkdir -p $B/dist/linux-x86_64 $B/dist/android-arm64-v8a
cp $(find /tmp/build-linux -name 010055D009F78000.so | head -1) $B/dist/linux-x86_64/
cp $(find /tmp/build-android -name 010055D009F78000.so | head -1) $B/dist/android-arm64-v8a/
$NDK/toolchains/llvm/prebuilt/linux-x86_64/bin/llvm-strip --strip-all $B/dist/linux-x86_64/010055D009F78000.so
$NDK/toolchains/llvm/prebuilt/linux-x86_64/bin/llvm-strip --strip-all $B/dist/android-arm64-v8a/010055D009F78000.so
ls -la $B/dist/*/ ; sha256sum $B/dist/*/*.so
echo BUILD_DONE
