from typing import Optional

from mysql.connector import MySQLConnection


def mysql_operation_cognition_add(conn: MySQLConnection, cognition_id: int, parent_id: int, owner_id: int,
                                  friend_id: int, type: int, input_content: str, output_content: str,
                                  is_related_to_previous: bool,
                                  model_parameters: Optional[str] = None, system_prompt: Optional[str] = None,
                                  input_tokens: Optional[int] = None, output_tokens: Optional[int] = None):
    """
    添加世界记录
    :param conn:
    :param cognition_id:
    :param parent_id:
    :param owner_id:
    :param friend_id:
    :param type:
    :param input_content:
    :param output_content:
    :param is_related_to_previous:
    :param model_parameters:
    :param system_prompt:
    :param input_tokens:
    :param output_tokens:
    :return:
    """
    fields = ["id", "parent_id", "owner_id", "friend_id", "type", "input_content", "output_content",
              "is_related_to_previous"]
    values = [cognition_id, parent_id, owner_id, friend_id, type, input_content, output_content, is_related_to_previous]
    placeholders = ["%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s"]

    if model_parameters is not None:
        fields.append("model_parameters")
        values.append(model_parameters)
        placeholders.append("%s")

    if system_prompt is not None:
        fields.append("system_prompt")
        values.append(system_prompt)
        placeholders.append("%s")

    if input_tokens is not None:
        fields.append("input_tokens")
        values.append(input_tokens)
        placeholders.append("%s")

    if output_tokens is not None:
        fields.append("output_tokens")
        values.append(output_tokens)
        placeholders.append("%s")

    operation = f"""INSERT INTO `cognition` ({', '.join(fields)}) VALUES ({', '.join(placeholders)})"""
    with conn.cursor(dictionary=True) as cursor:
        cursor.execute(operation, values)


def mysql_operation_cognition_get(conn: MySQLConnection, cognition_id: int):
    """
    获取世界记录
    :param conn:
    :param cognition_id:
    :return:
    """
    operation = """SELECT * FROM cognition WHERE id = %s AND is_delete = 0"""
    params = (cognition_id, )
    with conn.cursor(dictionary=True) as cursor:
        cursor.execute(operation, params)
        return cursor.fetchone()
