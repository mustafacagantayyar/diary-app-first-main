# İçe aktar
from flask import Flask, render_template,request, redirect,session,url_for
# Veri tabanı kitaplığını bağlama
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# SQLite'ı bağlama
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Veri tabanı oluşturma
db = SQLAlchemy(app)
app.secret_key = "rafa silva"
# Tablo oluşturma

class Card(db.Model):
    # Sütun oluşturma
    # id
    id = db.Column(db.Integer, primary_key=True)
    # Başlık
    title = db.Column(db.String(100), nullable=False)
    # Tanım
    subtitle = db.Column(db.String(300), nullable=False)
    # Metin
    text = db.Column(db.Text, nullable=False)
    # Kullacını ID si
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"), nullable=False)
    # Nesnenin ve kimliğin çıktısı
    def __repr__(self):
        return f'<Card {self.id}>'
    

# Görev #1. Kullanıcı tablosu oluşturun
class User(db.Model):
	# Sütunlar oluşturuluyor
	#id
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	# Giriş
	email = db.Column(db.String(100), nullable=False)
	# Şifre
	password = db.Column(db.String(30), nullable=False)



@app.route('/', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        form_email = request.form['email']
        form_password = request.form['password']
        
        # Kullanıcı doğrulama
        # Veritabanında email ve şifreye göre kullanıcıyı bul
        user = User.query.filter_by(email=form_email, password=form_password).first()
        
        if user:
            # Kullanıcı bulundu ve şifre doğruysa
            # Kullanıcının ID'sini oturuma kaydet
            session['user_id'] = user.id  # <-- Burası önemli!
            return redirect('/index')
        else:
            # Kullanıcı bulunamadı veya şifre yanlış
            error = 'Hatalı giriş veya şifre'
            return render_template('login.html', error=error)    
    else:
        # GET isteği ise, yani sayfa ilk yüklendiğinde
        return render_template('login.html') 

 
  
@app.route('/reg', methods=['GET','POST'])
def reg():
    if request.method == 'POST':
        email= request.form['email']
        password = request.form['password']
        
        #Görev #3 Kullanıcı verilerinin veri tabanına kaydedilmesini sağlayın
        user = User(email=email, password=password)
        db.session.add(user)    
        db.session.commit()

        
        return redirect('/')
    
    else:    
        return render_template('registration.html')

# İçerik sayfasını çalıştırma
@app.route('/index')
def index():
    user_id = session.get('user_id')  # Oturumdaki kullanıcı ID'sini alıyoruz
    if user_id:
        cards = Card.query.filter_by(user_id=user_id).order_by(Card.id).all()
    else:
        cards = []  # Giriş yoksa boş liste döndürebilirsin
    return render_template('index.html', cards=cards)

# Kayıt sayfasını çalıştırma
@app.route('/card/<int:id>')
def card(id):
    card = Card.query.get(id)

    return render_template('card.html', card=card)

# Giriş oluşturma sayfasını çalıştırma
@app.route('/create')
def create():
    return render_template('create_card.html')

# Giriş formu
@app.route('/form_create', methods=['GET','POST'])
def form_create():
    user_id = session.get('user_id') 

    #eğer kullanıcının user.id si yoksa 
    if not user_id:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title =  request.form['title']
        subtitle =  request.form['subtitle']
        text =  request.form['text']

        # Veri tabanına gönderilecek bir nesne oluşturma
        card = Card(title=title, subtitle=subtitle, text=text, user_id=user_id)

        db.session.add(card)
        db.session.commit()
        return redirect('/index')
    else:
        return render_template('create_card.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None) 
    return redirect(url_for('login'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)