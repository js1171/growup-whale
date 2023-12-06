import datetime

def get_time():
    return datetime.datetime.now().date()

def studyCheck(db, User, required_exp, studyType, user_email) :

    # 유저 이메일 받아오기, id 구하기
    email = user_email
    user_list = db.session.query(User).filter_by(email=email).first()

    # 한 번만 클릭 할 수 있도록 제어s
    user_date = user_list.starttime.date() if user_list.starttime else None
    cur_time = get_time()

    if cur_time == user_date :
        return {'success': False, 'message': '하루에 한 번만 누를 수 있음!'}
    
    # 오늘 날짜 기록
    user_list.starttime = cur_time
    db.session.add(user_list)
    db.session.commit()

    # 클릭한 버튼 찾아내기
    study_type = studyType

    # 해당 study_type에 경험치 추가해주기
    studytype_list = user_list.study_type_level
    if study_type=="blog" :
        studytype_list.blog_lv = studytype_list.blog_lv + 1
    elif study_type=="main" :
        studytype_list.main_lv = studytype_list.main_lv + 1
    elif study_type=="argorithm" :
        studytype_list.argorithm_lv = studytype_list.argorithm_lv + 1
    elif study_type=="cs" :
        studytype_list.cs_lv = studytype_list.cs_lv + 1
    elif study_type=="workout" :
        studytype_list.workout_lv = studytype_list.workout_lv + 1
    db.session.add(studytype_list)
    db.session.commit()

    # study_type 중에 제일 높은 숫자를 가진걸로 job 설정, 총 경험치, 레벨 구하기

    data = {
        'blog' : studytype_list.blog_lv,
        'algorithm' : studytype_list.argorithm_lv,
        'main' : studytype_list.main_lv,
        'cs' : studytype_list.cs_lv,
        'workout' : studytype_list.workout_lv
    }
    job = max(data, key=data.get)
    curExp = 0 if not user_list.whale.exp else user_list.whale.exp
    total_exp = curExp + 1
    level = int(user_list.whale.level)
    whale_list = user_list.whale
    if(required_exp <= total_exp):
        level += 1
        whale_list.job = job

    # job, 경험치, 레벨 DB에 기록 (whale -> level, exp)
    whale_list.level = level
    whale_list.exp = total_exp
    db.session.add(whale_list)
    db.session.commit()

    return {'success': True, 'message': '화이팅!'}