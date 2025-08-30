#!/usr/bin/env python3
"""
캄보디아 농업용어 모바일 학습 앱 - Flask Backend
Mobile Learning App for Cambodian Agricultural Terms
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory
import os
import sys
from datetime import datetime
import json

# 현재 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_term_manager import EnhancedAgriculturalTermManager

app = Flask(__name__, 
           template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'),
           static_folder=os.path.join(os.path.dirname(__file__), '..', 'static'))

app.secret_key = 'mobile_learning_app_secret_2024'

# 전역 매니저 인스턴스
enhanced_manager = EnhancedAgriculturalTermManager()

@app.route('/')
def index():
    """메인 페이지 - 기존 웹 인터페이스로 리다이렉트"""
    return redirect(url_for('mobile_app'))

@app.route('/mobile')
def mobile_app():
    """모바일 학습 앱 메인 페이지"""
    return render_template('mobile_learning_app.html')

@app.route('/mobile/improved')
def improved_mobile_app():
    """개선된 모바일 학습 앱"""
    return render_template('improved_mobile_app.html')

@app.route('/mobile/v3')
def agricultural_learning_v3():
    """참조 파일 기반 농업용어 학습 앱 V3"""
    return render_template('agricultural_learning_v3.html')

@app.route('/mobile/v3/5000')
def agricultural_learning_v3_5000():
    """5,000개 농업용어 학습 앱 V3"""
    return render_template('agricultural_learning_v3_5000.html')

@app.route('/mobile/v3/5000/optimized') 
def agricultural_learning_v3_5000_optimized():
    """5,000개 농업용어 학습 앱 V3 (성능 최적화)"""
    return render_template('agricultural_learning_v3_5000_optimized.html')
@app.route('/api/daily_words')
def api_daily_words():
    """일일 학습 단어 API"""
    try:
        day = int(request.args.get('day', 1))
        start = int(request.args.get('start', 0))
        limit = int(request.args.get('limit', 10))
        
        # 일일 단어 가져오기
        words = enhanced_manager.get_daily_words(day, limit)
        
        return jsonify({
            'success': True,
            'day': day,
            'words': words,
            'total_count': len(words)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/daily-words/<int:day>')
def api_daily_words_improved(day):
    """개선된 일일 학습 단어 API"""
    try:
        # 일일 단어 가져오기 (10개)
        words = enhanced_manager.get_daily_words(day, 10)
        
        # 개선된 앱에 맞는 형식으로 변환
        formatted_words = []
        for word in words:
            formatted_word = {
                'id': word.get('id'),
                'korean': word.get('korean_term', ''),
                'khmer': word.get('khmer_term', ''),
                'pronunciation': word.get('khmer_pronunciation', ''),
                'category': word.get('category', ''),
                'definition_ko': word.get('korean_definition', ''),
                'definition_km': word.get('khmer_definition', ''),
                'example_ko': word.get('korean_example', ''),
                'example_km': word.get('khmer_example', ''),
                'example_pronunciation': word.get('khmer_example_pronunciation', ''),
                'frequency': word.get('frequency_level', 3),
                'difficulty': word.get('difficulty_level', '중급'),
                'tags': word.get('tags', [])
            }
            formatted_words.append(formatted_word)
        
        return jsonify(formatted_words)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/words_by_category')
def api_words_by_category():
    """카테고리별 단어 API"""
    try:
        category = request.args.get('category', '')
        limit = request.args.get('limit')
        limit = int(limit) if limit else None
        
        words = enhanced_manager.get_words_by_category(category, limit)
        
        return jsonify({
            'success': True,
            'category': category,
            'words': words,
            'total_count': len(words)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/search_enhanced')
def api_search_enhanced():
    """확장된 검색 API"""
    try:
        keyword = request.args.get('keyword', '')
        category = request.args.get('category', '')
        difficulty = request.args.get('difficulty', '')
        frequency = int(request.args.get('frequency', 0))
        verified_only = request.args.get('verified_only') == 'true'
        limit = request.args.get('limit')
        limit = int(limit) if limit else None
        
        results = enhanced_manager.search_enhanced_terms(
            keyword=keyword,
            category=category,
            difficulty_level=difficulty,
            frequency_level=frequency,
            verified_only=verified_only,
            limit=limit
        )
        
        return jsonify({
            'success': True,
            'results': results,
            'count': len(results),
            'search_params': {
                'keyword': keyword,
                'category': category,
                'difficulty': difficulty,
                'frequency': frequency,
                'verified_only': verified_only
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/learning_statistics')
def api_learning_statistics():
    """학습 통계 API"""
    try:
        stats = enhanced_manager.get_learning_statistics()
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/categories')
def api_categories():
    """카테고리 목록 API"""
    return jsonify({
        'success': True,
        'categories': enhanced_manager.categories
    })

@app.route('/api/generate_sample_data')
def api_generate_sample_data():
    """샘플 데이터 생성 API (개발용)"""
    try:
        count = int(request.args.get('count', 100))
        enhanced_manager.generate_sample_enhanced_data(count)
        
        stats = enhanced_manager.get_learning_statistics()
        
        return jsonify({
            'success': True,
            'message': f'{count}개 샘플 데이터 생성 완료',
            'current_stats': stats
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# TTS 음성 생성 API (Web Speech API의 서버사이드 대안)
@app.route('/api/tts/<language>/<text>')
def api_text_to_speech(language, text):
    """텍스트 음성 변환 API"""
    # 실제 TTS 서비스 연동 필요 (Google Cloud TTS, Azure, 등)
    # 현재는 클라이언트 사이드 Web Speech API 사용
    return jsonify({
        'success': True,
        'message': 'TTS는 클라이언트 사이드에서 처리됩니다.',
        'language': language,
        'text': text
    })

# PWA 매니페스트
@app.route('/manifest.json')
def manifest():
    """PWA 매니페스트"""
    manifest_data = {
        "name": "캄보디아 농업용어 학습 앱",
        "short_name": "농업용어 학습",
        "description": "캄보디아어-한국어 농업용어 8000단어 학습 애플리케이션",
        "start_url": "/mobile",
        "display": "standalone",
        "background_color": "#f1f8e9",
        "theme_color": "#4CAF50",
        "orientation": "portrait",
        "icons": [
            {
                "src": "/static/images/icon-72x72.png",
                "sizes": "72x72",
                "type": "image/png"
            },
            {
                "src": "/static/images/icon-96x96.png", 
                "sizes": "96x96",
                "type": "image/png"
            },
            {
                "src": "/static/images/icon-128x128.png",
                "sizes": "128x128", 
                "type": "image/png"
            },
            {
                "src": "/static/images/icon-144x144.png",
                "sizes": "144x144",
                "type": "image/png"
            },
            {
                "src": "/static/images/icon-152x152.png",
                "sizes": "152x152",
                "type": "image/png"
            },
            {
                "src": "/static/images/icon-192x192.png",
                "sizes": "192x192",
                "type": "image/png"
            },
            {
                "src": "/static/images/icon-384x384.png",
                "sizes": "384x384",
                "type": "image/png"
            },
            {
                "src": "/static/images/icon-512x512.png",
                "sizes": "512x512",
                "type": "image/png"
            }
        ]
    }
    
    response = app.response_class(
        response=json.dumps(manifest_data),
        status=200,
        mimetype='application/json'
    )
    return response

# 서비스 워커
@app.route('/sw.js')
def service_worker():
    """서비스 워커 스크립트"""
    return send_from_directory(app.static_folder, 'js/sw.js')

# 관리자 도구
@app.route('/admin')
def admin_dashboard():
    """관리자 대시보드"""
    stats = enhanced_manager.get_learning_statistics()
    return render_template('admin_dashboard.html', stats=stats)

@app.route('/admin/add_term', methods=['GET', 'POST'])
def admin_add_term():
    """관리자 - 용어 추가"""
    if request.method == 'POST':
        try:
            # 폼 데이터 수집
            term_data = {
                'korean_term': request.form['korean_term'],
                'khmer_term': request.form['khmer_term'],
                'khmer_pronunciation': request.form['khmer_pronunciation'],
                'category': request.form['category'],
                'korean_definition': request.form['korean_definition'],
                'khmer_definition': request.form['khmer_definition'],
                'korean_example': request.form['korean_example'],
                'khmer_example': request.form['khmer_example'],
                'khmer_example_pronunciation': request.form['khmer_example_pronunciation'],
                'english_term': request.form.get('english_term', ''),
                'english_example': request.form.get('english_example', ''),
                'frequency_level': int(request.form.get('frequency_level', 3)),
                'difficulty_level': request.form.get('difficulty_level', '중급'),
                'tags': [tag.strip() for tag in request.form.get('tags', '').split(',') if tag.strip()],
                'mnemonics': request.form.get('mnemonics', ''),
                'cultural_notes': request.form.get('cultural_notes', '')
            }
            
            term_id = enhanced_manager.add_enhanced_term(**term_data)
            
            return jsonify({
                'success': True,
                'message': f'용어가 성공적으로 추가되었습니다. (ID: {term_id})',
                'term_id': term_id
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    # GET 요청 시 폼 표시
    categories = enhanced_manager.categories
    return render_template('admin_add_term.html', categories=categories)

@app.route('/admin/export_mobile_data')
def admin_export_mobile_data():
    """모바일 앱용 데이터 내보내기"""
    try:
        output_path = os.path.join(app.static_folder, 'data', 'mobile_app_data.json')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        success = enhanced_manager.export_for_mobile_app(output_path)
        
        if success:
            return jsonify({
                'success': True,
                'message': '모바일 앱 데이터 내보내기 완료',
                'file_path': '/static/data/mobile_app_data.json'
            })
        else:
            return jsonify({
                'success': False,
                'error': '데이터 내보내기 실패'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# 에러 핸들러
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({
        'success': False,
        'error': 'API 엔드포인트를 찾을 수 없습니다.'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': '서버 내부 오류가 발생했습니다.'
    }), 500

# CORS 헤더 추가 (개발용)
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

if __name__ == '__main__':
    print("🚀 캄보디아 농업용어 모바일 학습 앱을 시작합니다...")
    
    # 샘플 데이터 확인 및 생성
    stats = enhanced_manager.get_learning_statistics()
    print(f"📊 현재 용어 수: {stats['total_terms']:,}")
    
    if stats['total_terms'] < 100:
        print("📚 샘플 데이터 생성 중...")
        enhanced_manager.generate_sample_enhanced_data(200)
        print("✅ 샘플 데이터 생성 완료")
    
    print("📱 모바일 앱 URL: http://localhost:5000/mobile")
    print("🔧 관리자 페이지: http://localhost:5000/admin")
    print("📊 API 문서: http://localhost:5000/api/learning_statistics")
    
    # Flask 앱 실행
    app.run(host='0.0.0.0', port=5001, debug=False)