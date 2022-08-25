"""
自定义的分页组件
"""
from django.utils.safestring import mark_safe


class Pagination(object):

    # page_param="page"意思是获取页面里的 page 字段的值
    def __init__(self, request, queryset, page_size=10, page_param="page", plus=5):

        # 解决搜索后分页 url拼接参数
        import copy
        from django.http.request import QueryDict
        query_dict = copy.deepcopy(request.GET)
        query_dict._multable = True
        # self.query_dict 包含了原来所有的参数
        self.query_dict = query_dict
        self.page_param = page_param

        # 拿到 页数 page 和 页面大小 page_size
        page = request.GET.get(page_param, "1")
        if page.isdecimal():    # 如果page是十进制的数
            page = int(page)
        else:
            page = 1
        self.page = page
        self.page_size = page_size

        # 每一页的起始索引和结束索引
        self.start = (page - 1) * page_size
        self.end = page * page_size

        # 每一页的queryset
        self.page_queryset = queryset[self.start: self.end]

        # 数据总条数
        self.total_count = queryset.count()

        # 总页码
        total_page_count, div = divmod(self.total_count, page_size)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count

        # 显示前后 plus 页
        self.plus = plus

    def html(self):
        # 显示当前页的前五页,后五页
        if self.total_page_count <= 2 * self.plus + 1:
            # 数据库中的数据比较少,未达到11页
            if self.total_count == 0:
                start_page = 1
                end_page = self.total_page_count + 1
            else:
                start_page = 1
                end_page = self.total_page_count
        # 数据库中的数据大于11页
        else:
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1
            else:
                if(self.page + self.plus) > self.total_page_count:
                    start_page = self.total_page_count - 2 * self.plus
                    end_page = self.total_page_count
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus

        # 每一页的html标签
        page_str_list = []

        # 首页
        self.query_dict.setlist(self.page_param, [1])
        page_str_list.append('<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode()))

        # 上一页
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page - 1])
            prev = '<li><a class="active" href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [1])
            prev = '<li><a class="active" href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)


        for i in range(start_page, end_page + 1):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = '<li class="active"><a  href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)

        # 下一页
        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            next = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.total_page_count])
            next = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(next)

        page_string = mark_safe(" ".join(page_str_list))
        return page_string