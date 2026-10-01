from flask import Blueprint, jsonify, render_template, request

from app.database import lead_ekle, tum_leadler
from app.services.ai_service import ai_service, AIServiceError


# Normal web sayfalari icin Blueprint
pages_bp = Blueprint('pages', __name__)

# API endpointleri icin Blueprint
api_bp = Blueprint('api', __name__)


@pages_bp.route('/')
def index():
    """Karsilama sayfasini gosterir."""
    return render_template('index.html')


@pages_bp.route('/dashboard')
def dashboard():
    """Yonetim panelini gosterir."""
    return render_template('dashboard.html')


@api_bp.route('/sohbet', methods=['POST'])
def sohbet():
    """Kullanicinin mesajini yapay zekaya gonderir."""
    veri = request.get_json(silent=True) or {}

    mesaj = veri.get('mesaj', '').strip()
    gecmis = veri.get('gecmis', [])

    if not mesaj:
        return jsonify({'basari': False, 'hata': 'Mesaj bos olamaz.'}), 400

    try:
        cevap = ai_service.yanit_uret(mesaj, gecmis)
        return jsonify({'basari': True, 'cevap': cevap})

    except AIServiceError:
        return jsonify({
            'basari': False,
            'hata': 'Yapay zeka servisine su anda ulasilamiyor.'
        }), 503


@api_bp.route('/leads', methods=['POST'])
def yeni_lead():
    """Yeni bir iletisim kaydi olusturur."""
    veri = request.get_json(silent=True) or {}

    isim = veri.get('isim', '').strip()
    telefon = veri.get('telefon', '').strip()
    mesaj = veri.get('mesaj', '').strip()

    if not isim or not telefon:
        return jsonify({
            'basari': False,
            'hata': 'Isim ve telefon alanlari zorunludur.'
        }), 400

    lead_ekle(isim, telefon, mesaj)

    return jsonify({
        'basari': True,
        'mesaj': 'Kaydiniz basariyla olusturuldu.'
    }), 201


@api_bp.route('/leads', methods=['GET'])
def leadleri_getir():
    """Tum iletisim kayitlarini getirir."""
    leadler = tum_leadler()

    return jsonify({
        'basari': True,
        'leadler': leadler
    })