from flask import Flask, flash, render_template, request, redirect, url_for, session, make_response
from flask_mail import Mail, Message
import mysql.connector
import secrets
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = ""

#open connection
db_klt = {
    'host': '',
    'user': '',
    'password': '',
    'database': ''
}

def get_db_connection():
    """Create and return a new database connection."""
    return mysql.connector.connect(**db_klt)

#konfigurasi Flask-Email
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '@gmail.com'
app.config['MAIL_PASSWORD'] = ''

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/layanan')
def layanan():
    return render_template('layanan.html')

@app.route('/galeri')
def galeri():
    return render_template('galeri.html')

@app.route('/hubungi_kami')
def hubungi_kami():
    return render_template('hubungi_kami.html')

# --------- List bagian Penginapan -------------- #
@app.route('/penginapan')
def penginapan():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM penginapan")
    users = cursor.fetchall()
    cursor.close()
    print(users)
    conn.close()
    print(users)
    return render_template('penginapan.html', pg=users)

@app.route('/tambah/')
def tambah():
    return render_template('tambah.html')

@app.route('/proses_tambah/', methods=['POST'])
def proses_tambah():
    conn = get_db_connection()
    nama_lokasi = request.form['nama_lokasi']
    lokasi = request.form['lokasi']
    harga = request.form['harga']
    ulasan = request.form['ulasan']
    foto = request.form['foto']
    fasilitas = request.form['fasilitas']
    deskripsi = request.form['deskripsi']

    cur = conn.cursor()
    cur.execute("""
        INSERT INTO penginapan (nama_lokasi, lokasi, harga, ulasan, foto, fasilitas, deskripsi)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (nama_lokasi, lokasi, harga, ulasan, foto, fasilitas, deskripsi))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('penginapan'))


@app.route('/ubah/<id>', methods=['GET'])
def ubah(id):
    conn = get_db_connection() #cek koneksi
    cur = conn.cursor() #masuk ke database (tabel)
    cur.execute('SELECT * FROM penginapan WHERE id=%s', (id, ))
    res = cur.fetchall() #mengirim
    cur.close() #nutup koneksi database
    conn.close() #tutup koneksi
    return render_template('ubah.html', hasil=res)

@app.route('/proses_ubah/', methods=['POST'])
def proses_ubah():
    conn = get_db_connection()
    id = request.form['id']
    nama_lokasi = request.form['nama_lokasi']
    lokasi = request.form['lokasi']
    harga = request.form['harga']
    ulasan = request.form['ulasan']
    foto = request.form['foto']
    fasilitas = request.form['fasilitas']
    deskripsi = request.form['deskripsi']

    cur = conn.cursor()
    cur.execute("""
        UPDATE penginapan
        SET nama_lokasi=%s, lokasi=%s, harga=%s, ulasan=%s, foto=%s, fasilitas=%s, deskripsi=%s
        WHERE id=%s
    """, (nama_lokasi, lokasi, harga, ulasan, foto, fasilitas, deskripsi, id))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('penginapan'))


@app.route('/hapus/<id>', methods=['GET'])
def hapus(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM penginapan WHERE id=%s", (id, ))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('penginapan'))
# --------- Tutup List bagian Penginapan -------------- #

# --------- List bagian Wisata -------------- #
@app.route('/tempat_wisata')
def tempat_wisata():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM wisata")
    users = cursor.fetchall()
    cursor.close()
    print(users)
    conn.close()
    print(users)
    return render_template('wisata.html', rg=users)

@app.route('/tambahWisata/')  # sinkron ke tambah
def tambahWisata():
    return render_template('tambahWisata.html')

@app.route('/proses_tambahWisata/', methods=['POST'])  # sinkron ke proses tambah
def proses_tambahWisata():
    conn = get_db_connection()
    nama_tempat = request.form['nama_tempat']
    lokasi = request.form['lokasi']
    tiket = request.form['tiket']
    jam_buka = request.form['jam_buka']
    jam_tutup = request.form['jam_tutup']
    foto = request.form['foto']
    ulasan = request.form['ulasan']
    fasilitas = request.form['fasilitas']
    deskripsi = request.form['deskripsi']

    cur = conn.cursor()
    cur.execute('INSERT INTO wisata (nama_tempat, lokasi, tiket, jam_buka, jam_tutup, foto, ulasan, fasilitas, deskripsi) '
                'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                (nama_tempat, lokasi, tiket, jam_buka, jam_tutup, foto, ulasan, fasilitas, deskripsi))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('tempat_wisata'))


@app.route('/ubahWisata/<id>', methods=['GET'])  # sinkron ke ubahWisata
def ubahWisata(id):
    conn = get_db_connection()  # cek koneksi
    cur = conn.cursor()  # masuk ke database (tabel)
    cur.execute('SELECT * FROM wisata WHERE id=%s', (id, ))  # tabel database
    res = cur.fetchall()  # mengirim
    cur.close()  # nutup koneksi database
    conn.close()  # tutup koneksi
    return render_template('ubahWisata.html', hasil=res)


@app.route('/proses_ubahWisata/', methods=['POST'])
def proses_ubahWisata():
    conn = get_db_connection()
    id = request.form['id']
    nama_tempat = request.form['nama_tempat']
    lokasi = request.form['lokasi']
    tiket = request.form['tiket']
    jam_buka = request.form['jam_buka']
    jam_tutup = request.form['jam_tutup']
    foto = request.form['foto']
    ulasan = request.form['ulasan']
    fasilitas = request.form['fasilitas']
    deskripsi = request.form['deskripsi']

    cur = conn.cursor()
    cur.execute("UPDATE wisata SET nama_tempat=%s, lokasi=%s, tiket=%s, jam_buka=%s, jam_tutup=%s, foto=%s, "
                "ulasan=%s, fasilitas=%s, deskripsi=%s WHERE id=%s",
                (nama_tempat, lokasi, tiket, jam_buka, jam_tutup, foto, ulasan, fasilitas, deskripsi, id))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('tempat_wisata'))

@app.route('/hapusWisata/<id>', methods=['GET'])
def hapusWisata(id):
    cond = get_db_connection()
    cur = cond.cursor()
    cur.execute("DELETE FROM wisata WHERE id=%s", (id, ))
    cond.commit()
    cur.close()
    cond.close()
    return redirect(url_for('tempat_wisata'))
# --------- Tutup List bagian Wisata -------------- #


# --------- Open List bagian Kuliner -------------- #
@app.route('/kuliner')
def kuliner():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM kuliner")
    users = cursor.fetchall()
    cursor.close()
    print(users)
    conn.close()
    print(users)
    return render_template('kuliner.html', sg=users)

@app.route('/tambahKuliner/')  # Route for the add form
def tambahKuliner():
    return render_template('tambahKuliner.html')

@app.route('/proses_tambahKuliner/', methods=['POST'])  # Route for processing add form
def proses_tambahKuliner():
    conn = get_db_connection()
    tempat_kuliner = request.form['tempat_kuliner']
    lokasi = request.form['lokasi']
    tema = request.form['tema']
    status = request.form['status']
    foto = request.form['foto']
    ulasan = request.form['ulasan']
    fasilitas = request.form['fasilitas']
    deskripsi = request.form['deskripsi']

    cur = conn.cursor()
    cur.execute('''
        INSERT INTO kuliner (tempat_kuliner, lokasi, tema, status, foto, ulasan, fasilitas, deskripsi)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ''', (tempat_kuliner, lokasi, tema, status, foto, ulasan, fasilitas, deskripsi))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('kuliner'))

@app.route('/ubahKuliner/<id>', methods=['GET'])  # Route for the edit form
def ubahKuliner(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM kuliner WHERE id=%s', (id,))
    res = cur.fetchone()  # Using fetchone for a single record
    cur.close()
    conn.close()
    return render_template('ubahKuliner.html', hasil=res)

@app.route('/proses_ubahKuliner/', methods=['POST'])  # Route for processing edit form
def proses_ubahKuliner():
    conn = get_db_connection()
    id = request.form['id']
    tempat_kuliner = request.form['tempat_kuliner']
    lokasi = request.form['lokasi']
    tema = request.form['tema']
    status = request.form['status']
    foto = request.form['foto']
    ulasan = request.form['ulasan']
    fasilitas = request.form['fasilitas']
    deskripsi = request.form['deskripsi']

    cur = conn.cursor()
    cur.execute('''
        UPDATE kuliner
        SET tempat_kuliner=%s, lokasi=%s, tema=%s, status=%s, foto=%s, ulasan=%s, fasilitas=%s, deskripsi=%s
        WHERE id=%s
    ''', (tempat_kuliner, lokasi, tema, status, foto, ulasan, fasilitas, deskripsi, id))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('kuliner'))

@app.route('/hapusKuliner/<id>', methods=['GET'])
def hapusKuliner(id):
    cond = get_db_connection()
    cur = cond.cursor()
    cur.execute("DELETE FROM kuliner WHERE id=%s", (id, ))
    cond.commit()
    cur.close()
    cond.close()
    return redirect(url_for('kuliner'))

@app.route("/send_email", methods=["POST"])
def send_email():
    try:
        # Ambil data dari formulir
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        subject = request.form['subject']
        message = request.form['message']

        # Buat email
        msg = Message(
            subject=f"[Kontak Form] {subject}",
            sender=email,
            recipients=["@gmail.com", "@gmail.com", "@gmail.com"],  # Ganti dengan email admin
            body=f"Nama: {name}\nEmail: {email}\nTelepon: {phone}\n\nPesan:\n{message}"
        )

        # Kirim email
        mail.send(msg)
        flash("Pesan Anda berhasil dikirim!", "success")
    except Exception as e:
        flash(f"Terjadi kesalahan: {e}", "danger")

    return render_template("hubungi_kami.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        remember = request.form.get('remember')

        # Database connection
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        # Verifikasi user dan password
        if user and check_password_hash(user['password'], password):
            session['username'] = user['username']
            session['email'] = user['email']
            session['role'] = user['role']

            # Remember me
            if remember:
                response = make_response(redirect(url_for('index')))
                expires = datetime.now() + timedelta(days=30)
                response.set_cookie('username', user['username'], expires=expires)
                response.set_cookie('email', user['email'], expires=expires)
                response.set_cookie('role', user['role'], expires=expires)
                return response
            else:
                flash("Login berhasil!", "success")
                return redirect(url_for('index'))
        else:
            flash("Email atau password salah.", "danger")
            return redirect(url_for('login'))

    # Check cookies (Remember me)
    if 'username' in request.cookies:
        session['username'] = request.cookies.get('username')
        session['email'] = request.cookies.get('email')
        session['role'] = request.cookies.get('role')
        flash("Login berhasil dari Remember Me cookies!", "success")
        return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)",
                           (username, email, hashed_password, 'user'))
            conn.commit()
            cursor.close()
            conn.close()
            flash("Registrasi berhasil. Silakan login.", "success")
            return redirect(url_for('login'))
        except mysql.connector.IntegrityError:
            flash("Gagal melakukan registrasi. Email atau username sudah digunakan.", "danger")
    return render_template('register.html')

@app.route('/logout')
def logout():
    # Hapus session
    session.pop('username', None)
    session.pop('email', None)
    session.pop('role', None)

    # Hapus cookies yang digunakan oleh Remember Me
    response = make_response(redirect(url_for('login')))
    response.delete_cookie('username')
    response.delete_cookie('email')
    response.delete_cookie('role')

    flash("Anda telah logout.", "info")
    return response


if __name__ == '__main__':
    app.run(debug=True)