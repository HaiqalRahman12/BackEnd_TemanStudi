import json
import logging
import re
import os
from llama_cpp import Llama

# Setup Logger agar terlihat status proses di terminal
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("TemanStudi-AI")

class AIBackendEngine:
    def __init__(self, model_filename: str):
        # Cari lokasi file model secara otomatis
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        model_path = os.path.join(base_dir, "models", model_filename)

        if not os.path.exists(model_path):
            logger.error(f"❌ MODEL TIDAK DITEMUKAN DI: {model_path}")
            raise FileNotFoundError("Model file missing. Cek folder models!")

        logger.info(f"🚀 Memuat Model ke GPU: {model_filename}...")
        
        # KONFIGURASI VRAM RTX 3050 (4GB)
        self.llm = Llama(
            model_path=model_path,
            n_gpu_layers=-1,      # -1 = Paksa semua layer masuk VRAM GPU
            n_ctx=4096,           # Kapasitas memori konteks (token)
            n_batch=512,          # Batch size pemrosesan standar
            verbose=False,        # Matikan log spam C++
            chat_format="chatml"  # Format prompt native Qwen
        )
        
        # Setting Sliding Window (Chunking)
        self.chunk_size = 2000  # Karakter per proses (~400 kata)
        self.overlap = 300      # Irisan agar kalimat tidak putus di tengah

    def _create_grammar(self):
        """Pagar Listrik: Memaksa AI output JSON Array Strict"""
        return {
            "type": "json_object",
            "schema": {
                "type": "object",
                "properties": {
                    "flashcards": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "question": {"type": "string"},
                                "answer": {"type": "string"}
                            },
                            "required": ["question", "answer"]
                        }
                    }
                },
                "required": ["flashcards"]
            }
        }

    def _split_text(self, text: str) -> list[str]:
        """Memecah teks panjang menjadi potongan-potongan aman."""
        text = re.sub(r'\s+', ' ', text).strip() # Bersihkan spasi ganda
        chunks = []
        start = 0
        text_len = len(text)
        
        while start < text_len:
            end = start + self.chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start += self.chunk_size - self.overlap
            
        return chunks

    def generate_flashcards(self, full_text: str) -> list[dict]:
        chunks = self._split_text(full_text)
        logger.info(f"📚 Teks dipecah menjadi {len(chunks)} bagian (Chunks).")
        
        all_cards = []

        # PROMPT ENGINEERING (Kunci Kualitas)
        system_msg = """
        Anda adalah dosen senior yang kritis. 
        Tugas: Ekstrak intisari materi menjadi Flashcard (Tanya-Jawab).
        Aturan:
        1. Pertanyaan harus menguji pemahaman konsep, bukan hafalan buta.
        2. Gunakan Bahasa Indonesia Baku.
        3. Jawaban harus padat dan jelas.
        """

        # ONE-SHOT EXAMPLE (Agar AI meniru style analitis ini)
        example_user = "Teks: Fotosintesis mengubah energi cahaya menjadi energi kimia dalam bentuk glukosa menggunakan klorofil."
        example_assistant = json.dumps({
            "flashcards": [
                {"question": "Apa peran klorofil dalam proses transformasi energi?", "answer": "Menangkap energi cahaya matahari untuk diubah menjadi energi kimia."},
                {"question": "Apa produk akhir dari penyimpanan energi kimia pada fotosintesis?", "answer": "Glukosa."}
            ]
        })

        # LOOPING CHUNKS
        for i, chunk in enumerate(chunks):
            # Skip potongan yang terlalu pendek (biasanya sisa sampah di akhir)
            if len(chunk) < 150: continue

            try:
                logger.info(f"⚡ Sedang Memikirkan Chunk {i+1}/{len(chunks)}...")
                
                response = self.llm.create_chat_completion(
                    messages=[
                        {"role": "system", "content": system_msg},
                        {"role": "user", "content": example_user},           # Shot 1 Input
                        {"role": "assistant", "content": example_assistant}, # Shot 1 Output
                        {"role": "user", "content": f"Analisis teks ini dan buat 2-3 flashcard:\n\n{chunk}"}
                    ],
                    temperature=0.3, # Rendah agar tidak halusinasi
                    max_tokens=1024,
                    response_format=self._create_grammar() # JSON Enforcer
                )
                
                content = response['choices'][0]['message']['content']
                data = json.loads(content)
                new_cards = data.get("flashcards", [])
                
                # Filter Validasi Panjang Karakter
                for card in new_cards:
                    q = card.get('question', '')
                    a = card.get('answer', '')
                    if len(q) > 10 and len(a) > 2:
                        all_cards.append(card)
                        
            except Exception as e:
                logger.error(f"⚠️ Gagal pada chunk {i+1}: {str(e)}")
                continue

        logger.info(f"✅ Selesai! Total {len(all_cards)} kartu berhasil dibuat.")
        return all_cards

# SINGLETON PATTERN
_engine = None
def get_engine():
    global _engine
    if _engine is None:
        # NAMA FILE MODEL HARUS SESUAI
        _engine = AIBackendEngine("Qwen3-1.7B-Instruct-Q5_K_M.gguf")
    return _engine
