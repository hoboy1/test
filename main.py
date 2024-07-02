import tkinter as tk
import random

class DodgeGame:
    def __init__(self, master):
        self.master = master
        master.title("게임")
        self.width = 400
        self.height = 400
        self.canvas = tk.Canvas(master, width=self.width, height=self.height, bg="white")
        self.canvas.pack()
        
        # 점 설정
        self.dot_x = self.width // 2
        self.dot_y = self.height // 2
        self.dot_radius = 10
        self.dot = self.canvas.create_oval(
            self.dot_x - self.dot_radius,
            self.dot_y - self.dot_radius,
            self.dot_x + self.dot_radius,
            self.dot_y + self.dot_radius,
            fill="blue"
        )
        self.lives = 3
        self.lives_text = self.canvas.create_text(10, 10, anchor=tk.NW, text=f"Lives: {self.lives}")

        # 박스 설정
        self.box_size = 20
        self.boxes = []
        self.create_box()
        self.master.after(10000, self.create_box)  # 10초 후 첫 박스 생성

        # 키보드 이벤트 바인딩
        self.canvas.bind_all("<KeyPress-Up>", self.move_up)
        self.canvas.bind_all("<KeyPress-Down>", self.move_down)
        self.canvas.bind_all("<KeyPress-Left>", self.move_left)
        self.canvas.bind_all("<KeyPress-Right>", self.move_right)

        # 게임 루프 시작
        self.game_loop()

    def create_box(self):
        x = random.randint(0, self.width - self.box_size)
        y = random.randint(0, self.height - self.box_size)
        dx = random.choice([-4, -3, -2, 2, 3, 4])
        dy = random.choice([-4, -3, -2, 2, 3, 4])
        box = self.canvas.create_rectangle(x, y, x + self.box_size, y + self.box_size, fill="red")
        self.boxes.append((box, dx, dy))

    def move_boxes(self):
        for i, (box, dx, dy) in enumerate(self.boxes):
            self.canvas.move(box, dx, dy)
            x1, y1, x2, y2 = self.canvas.coords(box)
            
            # 벽 튕기기
            if x1 < 0 or x2 > self.width:
                dx *= -1
            if y1 < 0 or y2 > self.height:
                dy *= -1
            
            self.boxes[i] = (box, dx, dy)

    def check_collisions(self):
        dot_coords = self.canvas.coords(self.dot)
        for box, _, _ in self.boxes:
            box_coords = self.canvas.coords(box)
            if self.intersect(dot_coords, box_coords):
                self.lives -= 1
                self.canvas.itemconfig(self.lives_text, text=f"Lives: {self.lives}")
                if self.lives == 0:
                    self.game_over()
                break

    def intersect(self, coords1, coords2):
        x1, y1, x2, y2 = coords1
        x3, y3, x4, y4 = coords2
        return x1 < x4 and x2 > x3 and y1 < y4 and y2 > y3

    def game_over(self):
        self.canvas.create_text(self.width//2, self.height//2, text="Game Over", font=("Arial", 30))
        self.master.after(2000, self.master.destroy) 

    def move_up(self, event):
        self.canvas.move(self.dot, 0, -10)
        self.dot_y -= 10

    def move_down(self, event):
        self.canvas.move(self.dot, 0, 10)
        self.dot_y += 10

    def move_left(self, event):
        self.canvas.move(self.dot, -10, 0)
        self.dot_x -= 10

    def move_right(self, event):
        self.canvas.move(self.dot, 10, 0)
        self.dot_x += 10

    def game_loop(self):
        self.move_boxes()
        self.check_collisions()
        self.master.after(50, self.game_loop)

root = tk.Tk()
game = DodgeGame(root)
root.mainloop()