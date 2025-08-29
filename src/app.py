#!/usr/bin/env python3
"""
캄보디아 농업용어 3000단어 웹 애플리케이션
Agricultural Terms Web Application
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import os
import sys
from datetime import datetime

# 현재 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from term_manager import AgriculturalTermManager

app = Flask(__name__, 
           template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'),
           static_folder=os.path.join(os.path.dirname(__file__), '..', 'static'))
app.secret_key = 'agricultural_terms_secret_key_2024'

# 전역 매니저 인스턴스
manager = AgriculturalTermManager()

@app.route('/')
def index():
    """메인 페이지"""
    stats = manager.get_statistics()
    recent_terms = manager.search_terms()[-5:]  # 최근 5개 용어
    return render_template('index.html', stats=stats, recent_terms=recent_terms)

@app.route('/search')
def search():
    """검색 페이지"""
    keyword = request.args.get('keyword', '')
    category = request.args.get('category', '')
    difficulty = request.args.get('difficulty', '')
    verified_only = request.args.get('verified_only') == 'on'
    
    # 검색 실행
    results = manager.search_terms(
        keyword=keyword,
        category=category,
        difficulty_level=difficulty,
        verified_only=verified_only
    )
    
    # 카테고리 목록
    categories = manager.get_categories()
    
    return render_template('search.html', 
                         results=results, 
                         categories=categories,
                         search_params={
                             'keyword': keyword,
                             'category': category,
                             'difficulty': difficulty,
                             'verified_only': verified_only
                         })

@app.route('/term/<int:term_id>')
def view_term(term_id):
    """용어 상세보기"""
    term = manager.get_term_by_id(term_id)
    if not term:
        flash('해당 용어를 찾을 수 없습니다.', 'error')
        return redirect(url_for('index'))
    
    # 관련 용어들
    related_terms = []
    for related_id in term.get('related_terms', []):
        related_term = manager.get_term_by_id(related_id)
        if related_term:
            related_terms.append(related_term)
    
    return render_template('term_detail.html', term=term, related_terms=related_terms)

@app.route('/add_term', methods=['GET', 'POST'])
def add_term():
    """용어 추가"""
    if request.method == 'POST':
        try:
            # 폼 데이터 수집
            korean_term = request.form['korean_term'].strip()
            khmer_term = request.form['khmer_term'].strip()
            english_term = request.form.get('english_term', '').strip()
            category = request.form['category']
            korean_definition = request.form['korean_definition'].strip()
            khmer_definition = request.form['khmer_definition'].strip()
            usage_example = request.form.get('usage_example', '').strip()
            difficulty_level = request.form.get('difficulty_level', '중급')
            
            # 태그 처리 (쉼표로 분리)
            tags_input = request.form.get('tags', '').strip()
            tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
            
            # 필수 필드 검증
            if not all([korean_term, khmer_term, category, korean_definition, khmer_definition]):
                flash('필수 항목을 모두 입력해주세요.', 'error')
                return render_template('add_term.html', categories=get_categories_list())
            
            # 용어 추가
            term_id = manager.add_term(
                korean_term=korean_term,
                khmer_term=khmer_term,
                english_term=english_term,
                category=category,
                korean_definition=korean_definition,
                khmer_definition=khmer_definition,
                usage_example=usage_example,
                difficulty_level=difficulty_level,
                tags=tags
            )
            
            flash(f'용어 "{korean_term}"이 성공적으로 추가되었습니다!', 'success')
            return redirect(url_for('view_term', term_id=term_id))
            
        except Exception as e:
            flash(f'용어 추가 중 오류가 발생했습니다: {str(e)}', 'error')
    
    categories = get_categories_list()
    return render_template('add_term.html', categories=categories)

@app.route('/edit_term/<int:term_id>', methods=['GET', 'POST'])
def edit_term(term_id):
    """용어 편집"""
    term = manager.get_term_by_id(term_id)
    if not term:
        flash('해당 용어를 찾을 수 없습니다.', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        try:
            # 업데이트할 데이터 수집
            update_data = {
                'korean_term': request.form['korean_term'].strip(),
                'khmer_term': request.form['khmer_term'].strip(),
                'english_term': request.form.get('english_term', '').strip(),
                'category': request.form['category'],
                'korean_definition': request.form['korean_definition'].strip(),
                'khmer_definition': request.form['khmer_definition'].strip(),
                'usage_example': request.form.get('usage_example', '').strip(),
                'difficulty_level': request.form.get('difficulty_level', '중급'),
                'verified': 'verified' in request.form
            }
            
            # 태그 처리
            tags_input = request.form.get('tags', '').strip()
            update_data['tags'] = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
            
            # 용어 업데이트
            success = manager.update_term(term_id, **update_data)
            
            if success:
                flash(f'용어 "{update_data["korean_term"]}"이 성공적으로 수정되었습니다!', 'success')
                return redirect(url_for('view_term', term_id=term_id))
            else:
                flash('용어 수정에 실패했습니다.', 'error')
                
        except Exception as e:
            flash(f'용어 수정 중 오류가 발생했습니다: {str(e)}', 'error')
    
    categories = get_categories_list()
    return render_template('edit_term.html', term=term, categories=categories)

@app.route('/delete_term/<int:term_id>', methods=['POST'])
def delete_term(term_id):
    """용어 삭제"""
    term = manager.get_term_by_id(term_id)
    if not term:
        flash('해당 용어를 찾을 수 없습니다.', 'error')
        return redirect(url_for('index'))
    
    try:
        success = manager.delete_term(term_id)
        if success:
            flash(f'용어 "{term["korean_term"]}"이 삭제되었습니다.', 'success')
        else:
            flash('용어 삭제에 실패했습니다.', 'error')
    except Exception as e:
        flash(f'용어 삭제 중 오류가 발생했습니다: {str(e)}', 'error')
    
    return redirect(url_for('search'))

@app.route('/statistics')
def statistics():
    """통계 페이지"""
    stats = manager.get_statistics()
    return render_template('statistics.html', stats=stats)

@app.route('/api/search')
def api_search():
    """API: 용어 검색"""
    keyword = request.args.get('keyword', '')
    category = request.args.get('category', '')
    difficulty = request.args.get('difficulty', '')
    
    results = manager.search_terms(
        keyword=keyword,
        category=category,
        difficulty_level=difficulty
    )
    
    return jsonify({
        'success': True,
        'results': results,
        'count': len(results)
    })

@app.route('/api/statistics')
def api_statistics():
    """API: 통계 정보"""
    stats = manager.get_statistics()
    return jsonify(stats)

@app.route('/export/csv')
def export_csv():
    """CSV 파일로 내보내기"""
    try:
        output_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'agricultural_terms_export.csv')
        success = manager.export_to_csv(output_path)
        
        if success:
            flash('CSV 파일로 내보내기가 완료되었습니다.', 'success')
        else:
            flash('CSV 내보내기에 실패했습니다.', 'error')
            
    except Exception as e:
        flash(f'CSV 내보내기 중 오류가 발생했습니다: {str(e)}', 'error')
    
    return redirect(url_for('statistics'))

def get_categories_list():
    """카테고리 목록 반환"""
    return [
        "작물재배", "축산업", "농기계", "토양", "비료", "병해충",
        "수확", "저장", "가공", "유통", "농업정책", "농업경영",
        "원예", "임업", "수산업", "농업기술", "수자원", "농업시설",
        "종자", "농약", "기타"
    ]

if __name__ == '__main__':
    # 개발 모드에서 실행
    print("캄보디아 농업용어 사전 웹 애플리케이션을 시작합니다...")
    print("http://localhost:5000 에서 접속 가능합니다.")
    app.run(host='0.0.0.0', port=5000, debug=True)