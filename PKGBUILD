# Maintainer: Your Name <your.email@example.com>
pkgname=blippy
pkgver=1.0.0
pkgrel=1
pkgdesc="A little webcam viewer with reaction images and GIFs"
arch=('x86_64')
url="https://github.com/yourusername/blippy"
license=('MIT')
depends=('python' 'python-pygame' 'python-pillow' 'python-opencv')
makedepends=('pyinstaller')
source=("$pkgname-$pkgver.tar.gz::https://github.com/evanwmart/blippy/archive/refs/tags/v$pkgver.tar.gz")
sha256sums=('SKIP')

build() {
    cd "$srcdir/$pkgname-$pkgver"
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    pyinstaller --onefile --windowed blippy.py
}

package() {
    cd "$srcdir/$pkgname-$pkgver"
    install -Dm755 "dist/blippy" "$pkgdir/usr/bin/blippy"
    install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
}