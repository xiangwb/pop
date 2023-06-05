import random
from operator import itemgetter
from .model import UserSubject, Item, Point, PointRelation
from extensions import cache

import pysnooper

REPEATABLE_IIMES = 3


class FixedLengthList(list):
    def __init__(self, value: list, fixed_length: int):
        self._value = value
        self.fixed_length = fixed_length

    def __len__(self):
        return len(self.value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, _value):
        if len(_value) > self.fixed_length:
            self._value = _value[-self.fixed_length:]
        else:
            self._value = _value

    def append(self, item) -> None:
        if item not in self.value:
            if len(self.value) < self.fixed_length:
                self.value.append(item)
            else:
                self.value = self.value[1:]
                self.value.append(item)


def get_level():
    levels = ['undo'] * 4
    levels.extend(['doing'] * 5)
    levels.extend(['done'] * 1)
    level = random.choice(levels)
    return level


@pysnooper.snoop()
def get_order_item_ids(subject_id):
    item_ids_cache_key = 'subject_item_ids_{}'.format(subject_id)
    item_ids = cache.get(item_ids_cache_key)
    if not item_ids:
        item_ids = []
        first_level_point_relations = PointRelation.objects(subject_id=subject_id, from_node_type='subject').order_by(
            'sequence')
        for first_level_relation in first_level_point_relations:
            first_level_to_node_id = first_level_relation.to_node_id
            second_level_point_relations = PointRelation.objects(subject_id=subject_id,
                                                                 from_node_id=first_level_to_node_id) \
                .order_by('sequence')
            for second_level_relation in second_level_point_relations:
                second_level_to_node_id = second_level_relation.to_node_id
                items = Item.objects(point_id=second_level_to_node_id).order_by('sequence').only('id')
                items = [item.id for item in items]
                if items:
                    item_ids.extend(items)
    cache.set(item_ids_cache_key, item_ids, 24 * 60 * 60)
    return item_ids


@pysnooper.snoop()
def init_data(user_id, subject_id):
    item_ids = get_order_item_ids(subject_id)
    if item_ids:
        first_item_id = item_ids[0]
        current_item = Item.objects.get(id=first_item_id)
        UserSubject.objects.create(
            user_id=user_id,
            detail={
                'item_ids': item_ids,
                'values': [0] * len(item_ids),
                'current_index_id': 0,
                'current_item_id': first_item_id,
                'repeat_item_ids': []
            },
            subject_id=subject_id)
        return first_item_id, False
    else:
        # 不存在该课程,或者课程数据为空
        return None, True


@pysnooper.snoop(depth=1)
def get_next_item_id(user_id: str, subject_id: str, item_id: str = None, answer: str = None) -> tuple:
    pipeline = [{"$sample": {"size": 1}}] # $sample操作符用于随机获取记录
    try:
        random_record = Item.objects(subject_id=subject_id).aggregate(*pipeline).next() # 执行聚合操作
        return str(random_record['_id']),False
    except:
        return None, True
    # user_subject = UserSubject.objects(user_id=user_id, subject_id=subject_id).first()
    # # 存在学习记录
    # if user_subject:
    #     detail = user_subject.detail
    #     # 如果不提供item，意味着当前初次进入学习
    #     if item_id is None:
    #         # 已有学习记录，重新开始学习
    #         if detail:
    #             status = False
    #             current_item_id = detail.get('current_item_id')
    #             return current_item_id, status
    #         # 没有学习记录
    #         else:
    #             return init_data(user_id, subject_id)
    #     # 学习中
    #     else:
    #         status = False
    #         current_item_id = detail.get('current_item_id')
    #         item_ids = detail.get('item_ids')
    #         values = detail.get('values')
    #         repeat_item_ids = detail.get('repeat_item_ids')

    #         # 回答正确
    #         if answer:
    #             # 学习当前条目的相关条目后，返回相关知识点的下一条目
    #             if current_item_id != item_id:
    #                 # 更新detail
    #                 index_of_item_id = item_ids.index(item_id)
    #                 values[index_of_item_id] += 5
    #                 return current_item_id, False
    #             else:
    #                 # 更新detail
    #                 index_of_item_id = item_ids.index(item_id)
    #                 values[index_of_item_id] += 5
    #                 # 判断是否全部完成
    #                 if len([value for value in values if value >= 10]) == len(values):
    #                     item_id = current_item_id = None
    #                     status = True
    #                 else:
    #                     # 获取next_item_id
    #                     # 选择undo\doing\done
    #                     if len(item_ids) <= REPEATABLE_IIMES:
    #                         item_id = random.choice(item_ids)
    #                     else:
    #                         while 1:
    #                             level = get_level()
    #                             if level == 'undo':
    #                                 # if undo:
    #                                 #     item_id = current_item_id = undo[0]
    #                                 #     break
    #                                 try:
    #                                     index = values.index(0)
    #                                     item_id = item_ids[index]
    #                                 except ValueError:
    #                                     break
    #                             if level == 'doing':
    #                                 doing_item_ids = [item_id for (item_id, value) in zip(item_ids, values) if
    #                                                   0 < value < 10]
    #                                 if not doing_item_ids:
    #                                     break
    #                                 item_id = random.choice[doing_item_ids]
    #                             if level == 'done':
    #                                 done_item_ids = [item_id for (item_id, value) in zip(item_ids, values) if
    #                                                  value > 10]
    #                                 if not done_item_ids:
    #                                     break
    #                                 item_id = random.choice[done_item_ids]
    #                             if item_id in repeat_item_ids:
    #                                 break
    #             fll = FixedLengthList(repeat_item_ids, REPEATABLE_IIMES)
    #             fll.append(current_item_id)
    #             detail = {
    #                 'item_ids': item_ids,
    #                 'values': values,
    #                 'current_item_id': item_id,
    #                 'repeat_item_ids': fll.value
    #             }
    #             user_subject.detail = detail
    #             user_subject.save()
    #             return item_id, status
    #         # 上次回答错误
    #         else:
    #             # 学习当前条目的相关条目后，返回当前学习条目
    #             if current_item_id != item_id:
    #                 # 更新detail
    #                 index_of_item_id = item_ids.index(item_id)
    #                 values[index_of_item_id] += 2
    #                 return current_item_id, False
    #             else:
    #                 # 更新detail
    #                 index_of_item_id = item_ids.index(item_id)
    #                 values[index_of_item_id] += 2
    #                 item = Item.objects.get(id=item_id)
    #                 related_point_ids = item.related_point_ids
    #                 related_item_ids = list(Item.objects.filter(
    #                     point_id__in=related_point_ids,
    #                     type__in=['theory',
    #                               'general_knowledge']).only(
    #                     'id'))
    #                 if not related_item_ids:
    #                     # 选择下一个学习条目
    #                     # 选择undo\doing\done
    #                     if len(item_ids) <= REPEATABLE_IIMES:
    #                         item_id = random.choice(item_ids)
    #                     else:
    #                         while 1:
    #                             level = get_level()
    #                             if level == 'undo':
    #                                 # if undo:
    #                                 #     item_id = current_item_id = undo[0]
    #                                 #     break
    #                                 try:
    #                                     index = values.index(0)
    #                                     item_id = item_ids[index]
    #                                 except ValueError:
    #                                     break
    #                             if level == 'doing':
    #                                 doing_item_ids = [item_id for (item_id, value) in zip(item_ids, values) if
    #                                                   0 < value < 10]
    #                                 if not doing_item_ids:
    #                                     break
    #                                 item_id = random.choice[doing_item_ids]
    #                             if level == 'done':
    #                                 done_item_ids = [item_id for (item_id, value) in zip(item_ids, values) if
    #                                                  value > 10]
    #                                 if not done_item_ids:
    #                                     break
    #                                 item_id = random.choice[done_item_ids]
    #                             if item_id in repeat_item_ids:
    #                                 break
    #                 else:
    #                     related_items = [(item_id, value) for (item_id, value) in zip(item_ids, values) if
    #                                      item_id in related_item_ids]
    #                     sorted_related_items = sorted(related_items, key=itemgetter(1))
    #                     item_id = sorted_related_items[0][0]
    #             fll = FixedLengthList(repeat_item_ids, REPEATABLE_IIMES)
    #             fll.append(current_item_id)
    #             detail = {
    #                 'item_ids': item_ids,
    #                 'values': values,
    #                 'current_item_id': item_id,
    #                 'repeat_item_ids': fll.value
    #             }
    #             user_subject.detail = detail
    #             user_subject.save()
    #             return item_id, status
    # # 不存在学习记录
    # else:
    #     return init_data(user_id, subject_id)
