from flask import Flask, render_template


def create_app():
    from flask_app.module.dbModule import Database
    from flask_app.module.visualiser import Visualiser
    from flask_app.module.crawler import Crawler
    import datetime
    import time
    import atexit
    from apscheduler.schedulers.background import BackgroundScheduler

    app = Flask(__name__)

    scheduler = BackgroundScheduler()
    # scheduler.add_job(func=update_datebase, trigger="interval", hours=12)

    @scheduler.scheduled_job('cron', hour='09', minute='00', id='scraper')
    def update_datebase():
        crawler = Crawler()
        data = crawler.collect_naver_data()
        database = Database()
        database.update(data)
        print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))

    scheduler.start()

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())

    

    @app.route('/',methods=['GET'])
    def index():
        days = ["mon","tue","wed","thu","fri","sat","sun"]
        d = datetime.datetime.today().weekday()
        database = Database()
        query_list_all = f"""SELECT * FROM webtoons WHERE day='{days[d]}' ORDER BY rate DESC"""
        res = database.execute_all(query_list_all)
        database.db_close()
        # print(res)
        return render_template("index.html", res=res), 200
    
    # @app.route('/search/',defaults={'input':'추천 웹툰'}, methods=['GET'])
    @app.route('/search/<kw>',methods=['GET'])
    def search(kw):
        database = Database()
        query_list_all = f"""SELECT * FROM webtoons WHERE title LIKE '%%{kw}%%' ORDER BY rate DESC"""
        res = database.execute_all(query_list_all)
        database.db_close()
        # print(res)
        return render_template('search.html', kw=kw, res=res)
    
    @app.route('/dashboard/',methods=['GET'])
    def dashboard():
        database = Database()
        query_top1_views_day = f"""SELECT * FROM webtoons WHERE views_rank=1"""
        top1_views_day = database.execute_all(query_top1_views_day)

        query_top10_rate = f"""SELECT * FROM webtoons ORDER BY rate DESC LIMIT 10"""
        top10_rate = database.execute_all(query_top10_rate)

        query_count_genre = f"""
        SELECT genre, COUNT(*) 
        FROM webtoons 
        GROUP BY genre 
        ORDER BY COUNT(*) 
        LIMIT 10
        """
        count_genre = database.execute_all(query_count_genre)

        query_rank_genre = f"""
        SELECT sub.genre, COUNT(*)
        FROM (SELECT title, genre FROM webtoons WHERE views_rank < 20) AS sub
        GROUP BY sub.genre
        ORDER BY COUNT(*) DESC
        LIMIT 5"""
        rank_genre = database.execute_all(query_rank_genre)

        query_rate_genre = f"""
        SELECT genre, AVG(rate)
        FROM webtoons 
        GROUP BY genre
        ORDER BY AVG(rate) DESC
        """
        rate_genre = database.execute_all(query_rate_genre)
        

        database.db_close()

        visual = Visualiser()
        visual.pie(count_genre,"장르별 작품 수")
        visual.hbar(rank_genre,"장르별 인기도")
        visual.vbar(rate_genre,"장르별 평균 별점")
        
        return render_template('dashboard.html', 
                                top1_views_day=top1_views_day,
                                top10_rate=top10_rate,
                                )

    @app.route('/weekday/',defaults={'day':'mon'}, methods=['GET'])
    @app.route('/weekday/<day>', methods=['GET'])
    def weekday(day):
        days_kr = {
            "mon":"월",
            "tue":"화",
            "wed":"수",
            "thu":"목",
            "fri":"금",
            "sat":"토",
            "sun":"일"
            }

        database = Database()
        query_list_all = f"""SELECT * FROM webtoons WHERE day='{day}' ORDER BY rate DESC"""
        res = database.execute_all(query_list_all)
        database.db_close()

        return render_template('weekday.html',res=res, day=days_kr[day])

    @app.route('/about/', methods=['GET'])
    def about():
        return render_template('about.html')

    @app.route('/contact/', methods=['GET'])
    def contact():
        return render_template('contact.html')

    if __name__ == '__main__':
        app.run(debug=True)

    return app