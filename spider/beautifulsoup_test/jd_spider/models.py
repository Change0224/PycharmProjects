from peewee import  *

db = MySQLDatabase('myPython',host='localhost',port=3306,user='root',password='Change0224')


class BaseModel(Model):
    class Meta():
        database = db

class Good(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField(max_length=500, verbose_name="标题")
    content = TextField(default="", verbose_name="内容描述")
    supplier = CharField(max_length=500, verbose_name="发货方")
    ggbz = TextField(default="", verbose_name="规格与包装")
    image_list = TextField(default="", verbose_name="图片列表")
    price = FloatField(default=0.0, verbose_name="价格")
    good_rate = IntegerField(default=0,verbose_name="好评率")
    comments_nums = IntegerField(default=0, verbose_name="评论数")
    has_image_comment_nums = IntegerField(default=0, verbose_name="晒图数")
    has_video_comment_nums = IntegerField(default=0, verbose_name="视频晒单数")
    has_add_comment_nums = IntegerField(default=0, verbose_name="追评数")
    well_comment_nums = IntegerField(default=0, verbose_name="好评数")
    middle_comment_nums = IntegerField(default=0, verbose_name="中评数")
    bad_comment_nums = IntegerField(default=0, verbose_name="差评数")


class GoodEvaluate(BaseModel):
    id = CharField(primary_key=True)
    good = ForeignKeyField(Good, verbose_name="商品")
    user_head_url = CharField(verbose_name="用户头像")
    user_name = CharField(verbose_name="用户名")
    get_info = CharField(max_length=500, verbose_name="购买的商品信息")
    evaluate_time = DateTimeField()
    content = TextField(default="", verbose_name="评论内容")
    star = IntegerField(default=0, verbose_name="评分")
    comment_num = IntegerField(default=0, verbose_name="评论数")
    praised_num = IntegerField(default=0, verbose_name="点赞数")
    image_list = TextField(default="")
    video_list = TextField(default="")

class GoodEvaluateSummary(BaseModel):
    good = ForeignKeyField(Good, verbose_name="商品")
    tag = CharField(max_length=20, verbose_name="标签")
    num = IntegerField(default=0, verbose_name="数量")


if __name__ == '__main__':
    db.drop_tables([Good, GoodEvaluate, GoodEvaluateSummary])
    db.create_tables([Good, GoodEvaluate, GoodEvaluateSummary])