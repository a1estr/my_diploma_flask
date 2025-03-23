import allure
from tests.ui.pages.tasks_page import TasksPage
from tests.ui.pages.create_task_page import CreateTaskPage
from tests.ui.pages.edit_task_page import EditTaskPage
from tests.ui.pages.view_task_page import ViewTaskPage
from tests.data.task_data import task_data_ui, updated_task_data_ui


@allure.feature("Задачи (Tasks)")
@allure.story("Управление задачами")
@allure.title("Основные операции с задачами (CRUD) через UI")
@allure.severity(allure.severity_level.BLOCKER)
@allure.tag("UI", "Tasks", "CRUD")
def test_task_management(driver_login):
    """
    Тест проверяет основные операции с задачами через UI
    """
    # Выполним вход в систему с заранее зарегистрированным пользователем
    with allure.step("Вход в систему"):
        tasks_page = TasksPage(driver_login)
        tasks_page.attach_screenshot(
            tasks_page.FLASH_MESSAGE_SUCCESS,
            "Tasks page after login"
        )
        assert "tasks" in driver_login.current_url, \
            "Вход в систему не выполнен"

    # Создадим новую задачу
    with allure.step("Создание новой задачи"):
        # Перейдем на страницу создания новой задачи
        with allure.step("Редирект на страницу создания задачи"):
            tasks_page.click_create_task_button()
            create_task_page = CreateTaskPage(driver_login)
            create_task_page.attach_screenshot(
                create_task_page.TASK_HEADER,
                "Opened page with create task form"
            )
            assert "create" in driver_login.current_url, \
                "Страница создания новой задачи не открылась"

        # Заполним имя и описание задачи
        with allure.step("Заполнение имени и описания задачи"):
            create_task_page.enter_title(task_data_ui["title"])
            create_task_page.enter_description(task_data_ui["description"])
            create_task_page.attach_screenshot(
                create_task_page.TASK_HEADER,
                "Filled task form"
            )

        # Отправим заполненную форму
        with allure.step("Отправка заполненной формы"):
            create_task_page.click_submit_button()

        # Проверим сообщение об успешном создании задачи
        with allure.step("Сообщение об успешном создании задачи"):
            tasks_page.attach_screenshot(
                tasks_page.FLASH_MESSAGE_SUCCESS,
                "Tasks page with created task"
            )
            create_task_message = tasks_page.get_flash_success_message()
            expected_task_message = "Задача успешно создана"
            assert create_task_message == expected_task_message, \
                (f"Полученное сообщение о создании задачи:"
                 f"\n {create_task_message}\n"
                 f"Не соответствует ожидаемому:"
                 f"\n {expected_task_message}")

        # Проверим, что задача появилась в списке
        with allure.step("Появление новой задачи в списке"):
            task_title = task_data_ui["title"]
            titles_list = tasks_page.get_task_titles_list()
            assert task_title in titles_list, \
                f'Созданной задачи "{task_title}" нет в списке задач'

    # Отредактируем созданную задачу
    with allure.step("Редактирование задачи"):
        # Перейдем на страницу редактирования задачи
        with allure.step("Редирект на страницу создания задачи"):
            tasks_page.click_edit_button(task_data_ui["title"])
            edit_task_page = EditTaskPage(driver_login)
            edit_task_page.attach_screenshot(
                edit_task_page.COMPLETED_CHECKBOX,
                "Opened page with task edit form"
            )
            assert "edit" in driver_login.current_url, \
                "Страница редактирования задачи не открылась"

        # Отредактируем имя и описание задачи
        with allure.step("Редактирование имени и описания задачи"):
            edit_task_page.clear_fields()
            edit_task_page.enter_title(updated_task_data_ui["title"])
            edit_task_page.enter_description(
                updated_task_data_ui["description"]
            )
            edit_task_page.attach_screenshot(
                edit_task_page.COMPLETED_CHECKBOX,
                "Edited task title and description"
            )

        # Отправим отредактированную форму
        with allure.step("Отправка отредактированной формы"):
            edit_task_page.click_submit_button()

        # Проверим сообщение об успешном редактировании задачи
        with allure.step("Сообщение об успешном редактировании задачи"):
            tasks_page.attach_screenshot(
                tasks_page.FLASH_MESSAGE_SUCCESS,
                "Tasks page with updated task"
            )
            updated_task_message = tasks_page.get_flash_success_message()
            expected_task_message = "Задача успешно обновлена"
            assert updated_task_message == expected_task_message, \
                (f"Полученное сообщение о обновлении задачи:"
                 f"\n {updated_task_message}\n"
                 f"Не соответствует ожидаемому:"
                 f"\n {expected_task_message}")

        # Убедимся, что изменения сохранены
        with allure.step("Просмотр отредактированной задачи"):
            # Перейдем на страницу просмотра задачи
            with allure.step("Редирект на страницу просмотра задачи"):
                tasks_page.click_view_button(updated_task_data_ui["title"])
                view_task_page = ViewTaskPage(driver_login)
                view_task_page.attach_screenshot(
                    view_task_page.TASK_STATUS,
                    "View page with edited task"
                )

            # Сверим содержимое задачи
            with allure.step("Проверка содержимого задачи"):
                actual_task_title = view_task_page.get_title()
                expected_task_title = updated_task_data_ui["title"]
                assert actual_task_title == expected_task_title, \
                    (f"Имя задачи:\n {actual_task_title}\n"
                     f"Не соответствует ожидаемому:\n {expected_task_title}")

                actual_task_description = view_task_page.get_description()
                expected_task_description = updated_task_data_ui["description"]
                assert actual_task_description == expected_task_description, \
                    (f"Описание задачи:\n"
                     f"{actual_task_description}\n"
                     f"Не соответствует ожидаемому:\n"
                     f"{expected_task_description}")

    # Изменим статус задачи
    with allure.step("Изменение статуса задачи"):
        # На странице просмотра задачи отметим задачу как выполненную
        with allure.step("Нажатие кнопки изменения статуса задачи"):
            view_task_page.toggle_status()
            tasks_page.attach_screenshot(
                tasks_page.FLASH_MESSAGE_SUCCESS,
                "Task page with completed task"
            )

        # Проверим сообщение об успешном изменении статуса задачи
        with allure.step("Сообщение об успешном изменении статуса задачи"):
            complete_message = tasks_page.get_flash_success_message()
            expected_complete_message = "Задача отмечена как выполнена"
            assert complete_message == expected_complete_message, \
                (f"Полученное сообщение о изменении статуса задачи:"
                 f"\n {complete_message}\n"
                 f"Не соответствует ожидаемому:"
                 f"\n {expected_complete_message}")

        # Проверим, что статус изменился
        with allure.step("Проверка изменения статуса задачи"):
            tasks_page.click_view_button(updated_task_data_ui["title"])
            task_status = view_task_page.get_task_status()
            view_task_page.attach_screenshot(
                view_task_page.TASK_STATUS,
                "Task with completed status"
            )
            assert task_status == "Статус: Выполнено", \
                "Задача отмечена как невыполненная"

    # Удалим задачу
    with allure.step("Удаление задачи"):
        # Нажмем кнопку удаления задачи
        with allure.step("Нажатие кнопки удаления задачи"):
            view_task_page.click_delete_button()

        # Подтвердим удаление задачи
        with allure.step("Подтверждение удаления задачи"):
            view_task_page.attach_screenshot(
                view_task_page.DELETE_CONFIRM_BUTTON,
                "Confirming deletion"
            )
            view_task_page.click_delete_confirm_button()

        # Проверим, что задача была удалена
        with allure.step("Сообщение об успешном удалении задачи"):
            tasks_page.attach_screenshot(
                tasks_page.FLASH_MESSAGE_SUCCESS,
                "Successful deletion of task"
            )
            delete_message = tasks_page.get_flash_success_message()
            expected_delete_message = "Задача успешно удалена"
            assert delete_message == expected_delete_message, \
                (f"Полученное сообщение о удалении задачи:"
                 f"\n {delete_message}\n"
                 f"Не соответствует ожидаемому:"
                 f"\n {expected_delete_message}")

        with allure.step("Проверка, что задача исчезла из списка"):
            deleted_task_title = updated_task_data_ui["title"]
            tasks_list = tasks_page.get_task_titles_list()
            assert deleted_task_title not in tasks_list, \
                (f'Удаленная задача "{updated_task_data_ui["title"]}"'
                 f' все еще есть в списке')
