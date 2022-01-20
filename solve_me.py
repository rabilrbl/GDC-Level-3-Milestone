from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs


class TasksCommand:
    TASKS_FILE = "tasks.txt"
    COMPLETED_TASKS_FILE = "completed.txt"

    current_items = {}
    completed_items = []

    def read_current(self):
        try:
            file = open(self.TASKS_FILE, "r")
            for line in file.readlines():
                item = line[:-1].split(" ")
                self.current_items[int(item[0])] = " ".join(item[1:])
            file.close()
        except Exception:
            pass

    def read_completed(self):
        try:
            file = open(self.COMPLETED_TASKS_FILE, "r")
            self.completed_items = file.readlines()
            file.close()
        except Exception:
            pass

    def write_current(self):
        with open(self.TASKS_FILE, "w+") as f:
            f.truncate(0)
            for key in sorted(self.current_items.keys()):
                f.write(f"{key} {self.current_items[key]}\n")

    def write_completed(self):
        with open(self.COMPLETED_TASKS_FILE, "w+") as f:
            f.truncate(0)
            for item in self.completed_items:
                f.write(f"{item}\n")

    def runserver(self):
        address = "127.0.0.1"
        port = 8000
        server_address = (address, port)
        httpd = HTTPServer(server_address, TasksServer)
        print(f"Started HTTP Server on http://{address}:{port}")
        httpd.serve_forever()

    def run(self, command, args):
        self.read_current()
        self.read_completed()
        if command == "add":
            self.add(args)
        elif command == "done":
            self.done(args)
        elif command == "delete":
            self.delete(args)
        elif command == "ls":
            self.ls()
        elif command == "report":
            self.report()
        elif command == "runserver":
            self.runserver()
        elif command == "help":
            self.help()

    def help(self):
        print(
            """Usage :-
$ python tasks.py add 2 hello world # Add a new item with priority 2 and text "hello world" to the list
$ python tasks.py ls # Show incomplete priority list items sorted by priority in ascending order
$ python tasks.py del PRIORITY_NUMBER # Delete the incomplete item with the given priority number
$ python tasks.py done PRIORITY_NUMBER # Mark the incomplete item with the given PRIORITY_NUMBER as complete
$ python tasks.py help # Show usage
$ python tasks.py report # Statistics
$ python tasks.py runserver # Starts the tasks management server"""
        )

    def add(self, args):
        self.read_current()
        if len(args) < 2:
            print("Error: Missing tasks string. Nothing added!")
            return
        priority = int(args[0])
        name = " ".join(args[1:])
        if priority in self.current_items.keys():
            newPriority  = priority+1
            while newPriority in self.current_items.keys():
                newPriority += 1
            self.current_items[newPriority] = self.current_items.get(priority)
        self.current_items[priority] = name
        self.write_current()
        print(f"Added task: \"{name}\" with priority {priority}")
            

    def done(self, args):
        if len(args) < 1:
            print("Error: Missing priority number. Nothing done!")
            return
        priority = int(args[0])
        if priority in self.current_items.keys():
            self.completed_items.append(self.current_items.get(priority))
            del self.current_items[priority]
            self.write_current()
            self.write_completed()
            print("Marked item as done.")
        else:
            print(f"Error: no incomplete item with priority {priority} exists.")

    def delete(self, args):
        if len(args) < 1:
            print("Error: Missing priority number. Nothing deleted!")
            return
        priority = int(args[0])
        if priority in self.current_items.keys():
            del self.current_items[priority]
            self.write_current()
            print(f"Deleted item with priority {priority}.")
        else:
            print(f"Error: item with priority {args[0]} does not exist. Nothing deleted.")

    def ls(self):
        if len(self.current_items) == 0:
            print("No items in the list!")
            return
        for index,key in enumerate(sorted(self.current_items.keys()),1):
            print(f"{index}. {self.current_items[key]} [{key}]")

    def report(self):
        if len(self.current_items) == 0:
            print("No items in the list!")
            return
        print(f"Pending : {len(self.current_items)}")
        for index,key in enumerate(sorted(self.current_items.keys()),1):
            print(f"{index}. {self.current_items[key]} [{key}]")
        print(f"\nCompleted : {len(self.completed_items)}")
        for index,item in enumerate(self.completed_items,1):
            print(f"{index}. {item}")

    def render_pending_tasks(self):
        # Complete this method to return all incomplete tasks as HTML
        self.read_current()
        tasks = ""
        for p,t in self.current_items.items():
            tasks += f"<li>{t} [{p}]</li>"
        result = f"""<h1>Pending Tasks</h1>
                    <ul>
                        {tasks}
                    </ul>"""
        return result

    def render_completed_tasks(self):
        # Complete this method to return all completed tasks as HTML
        self.read_completed()
        completed = ""
        for t in self.completed_items:
            completed += f"<li>{t}</li>"
        result = f"""<h1>Completed Tasks</h1>
                    <ul>
                        {completed}
                    </ul>"""
        return result
    
    def render_add_task(self):
        # Complete this method to return the HTML for the add task form
        result = f"""<h1>Add Task</h1>
                    <form action="/add_task" method="post">
                        <input type="text" name="priority" placeholder="Priority">
                        <input type="text" name="task" placeholder="Task">
                        <input type="submit" value="Add">
                    </form>"""
        return result
    
    def render_done_task(self):
        # Complete this method to return the HTML for the done task form
        result = f"""<h1>Done Task</h1>
                    <form action="/done_task" method="post">
                        <input type="text" name="priority" placeholder="Priority">
                        <input type="submit" value="Done">
                    </form>"""
        return result
    
    def render_delete_task(self):
        # Complete this method to return the HTML for the delete task form
        result = f"""<h1>Delete Task</h1>
                    <form action="/delete_task" method="post">
                        <input type="text" name="priority" placeholder="Priority">
                        <input type="submit" value="Delete">
                    </form>"""
        return result
    
    def render_index(self):
        # Complete this method to return the HTML for the index page
        self.read_current()
        self.read_completed()
        tasks = ""
        for p,t in sorted(self.current_items.items()):
            tasks += f"<li><h3>{t} [{p}]</h3></li>"
        pendingTaskPage = f"""<h1>Pending Tasks</h1>
                    <ol>
                        {tasks}
                    </ol>"""
        completed = ""
        for t in self.completed_items:
            completed += f"<li>{t}</li>"
        compeltedTaskPage = f"""<h1>Completed Tasks</h1>
                    <ul>
                        {completed}
                    </ul>"""
        result = f"""<h1>Tasks</h1>
                    {pendingTaskPage}
                    {compeltedTaskPage}
                    <br>
                    <form action="/add_task" method="post">
                        <input type="text" name="priority" placeholder="Priority">
                        <input type="text" name="task" placeholder="Task">
                        <input type="submit" value="Add">
                    </form>
                    <form action="/done_task" method="post">
                        <input type="text" name="priority" placeholder="Priority">
                        <input type="submit" value="Done">
                    </form>
                    <form action="/delete_task" method="post">
                        <input type="text" name="priority" placeholder="Priority">
                        <input type="submit" value="Delete">
                    </form>
                    """
        return result


class TasksServer(TasksCommand, BaseHTTPRequestHandler):
    def do_GET(self):
        task_command_object = TasksCommand()
        if self.path == "/tasks":
            content = task_command_object.render_pending_tasks()
        elif self.path == "/completed":
            content = task_command_object.render_completed_tasks()
        elif self.path == "/add":
            # Complete this method to return the HTML for the add task form
            content = task_command_object.render_add_task()
        elif self.path == "/done":
            content = task_command_object.render_done_task()
        elif self.path == "/delete":
            content = task_command_object.render_delete_task()
        elif self.path == "/":
            content = task_command_object.render_index()
        else:
            self.send_response(404)
            self.end_headers()
            return
        self.send_response(200)
        self.send_header("content-type", "text/html")
        self.end_headers()
        self.wfile.write(content.encode())
    
    def do_POST(self):
        task_command_object = TasksCommand()
        if self.path == "/add_task":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length).decode()
            formResponse = parse_qs(post_data)
            task = formResponse["task"][0]
            priority = formResponse["priority"][0]
            task_command_object.add([ priority, task ])
            self.send_response(303)
            self.send_header("Location", "/")
            self.end_headers()
        elif self.path == "/done_task":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length).decode()
            formResponse = parse_qs(post_data)
            priority = formResponse["priority"][0]
            task_command_object.done([ priority ])
            self.send_response(303)
            self.send_header("Location", "/")
            self.end_headers()
        elif self.path == "/delete_task":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length).decode()
            formResponse = parse_qs(post_data)
            priority = formResponse["priority"][0]
            task_command_object.delete([ priority ])
            self.send_response(303)
            self.send_header("Location", "/")
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
            return

httpd = HTTPServer(("", 8000), TasksServer)
httpd.serve_forever()