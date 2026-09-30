import requests
from flask import current_app

class AIServiceError(Exception):
    """Yapay zeka servisinde bir sorun oldugunda firlatilir."""
    pass

class AIService:
    """Groq yapay zeka servisiyle konusan katman."""

    def _sistem_talimati_olustur(self):
        return current_app.config.get('BUSINESS_CONTEXT', 'Sen yardimci bir asistansin.')

    def _groq_cagir(self, mesaj, gecmis):
        api_key = current_app.config.get('GROQ_API_KEY', '')

        if not api_key:
            return self._demo_yaniti_ver()

        mesajlar = [{'role': 'system', 'content': self._sistem_talimati_olustur()}]
        mesajlar.extend(gecmis)
        mesajlar.append({'role': 'user', 'content': mesaj})

        try:
            yanit = requests.post(
                'https://api.groq.com/openai/v1/chat/completions',
                headers={'Authorization': f'Bearer {api_key}'},
                json={
                    'model': 'openai/gpt-oss-20b',
                    'messages': mesajlar
                },
                timeout=15
            )
            yanit.raise_for_status()
            veri = yanit.json()
            return veri['choices'][0]['message']['content']
        except requests.exceptions.RequestException as e:
            raise AIServiceError(f'Yapay zeka servisine ulasilamadi: {e}')

    def _demo_yaniti_ver(self):
        return ('Sistem demo modunda calisiyor. Gercek yanitlar icin '
                'lutfen .env dosyanizdaki GROQ_API_KEY degerini kontrol edin.')

    def yanit_uret(self, mesaj, gecmis=None):
        if gecmis is None:
            gecmis = []
        return self._groq_cagir(mesaj, gecmis)

ai_service = AIService()