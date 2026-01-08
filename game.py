import cv2
import mediapipe as mp
import numpy as np
import random
import math
import time

# -------------------- CAMERA --------------------
cap = cv2.VideoCapture(0)
WIDTH, HEIGHT = 1280, 720
cap.set(3, WIDTH)
cap.set(4, HEIGHT)

# -------------------- MEDIAPIPE --------------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# -------------------- GAME STATE --------------------
objects = []
particles = []
score = 0
lives = 5

combo = 1
last_hit_time = 0

difficulty = 1.0
spawn_rate = 0.03

last_shot = 0
game_over = False

# -------------------- OBJECT --------------------
class GameObject:
    def __init__(self):
        self.x = random.randint(100, WIDTH - 100)
        self.y = HEIGHT + random.randint(50, 200)
        self.size = random.randint(25, 50)
        self.speed = random.uniform(3, 5) * difficulty
        self.angle = random.uniform(-1, 1)
        self.color = random.choice([
            (255, 50, 50),
            (255, 255, 255),
            (255, 100, 100)
        ])
        self.shape = random.choice(["circle", "square", "triangle"])

    def move(self):
        self.y -= self.speed
        self.x += self.angle * 2

    def draw(self, img):
        if self.shape == "circle":
            cv2.circle(img, (int(self.x), int(self.y)), self.size, self.color, -1)
        elif self.shape == "square":
            cv2.rectangle(
                img,
                (int(self.x - self.size), int(self.y - self.size)),
                (int(self.x + self.size), int(self.y + self.size)),
                self.color,
                -1
            )
        else:
            pts = np.array([
                [self.x, self.y - self.size],
                [self.x - self.size, self.y + self.size],
                [self.x + self.size, self.y + self.size]
            ], np.int32)
            cv2.fillPoly(img, [pts], self.color)

# -------------------- PARTICLE --------------------
class Particle:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.vx = random.uniform(-5, 5)
        self.vy = random.uniform(-5, 5)
        self.life = random.randint(15, 25)

    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

# -------------------- FIRE GESTURE --------------------
def fire_gesture(hand):
    index = hand.landmark[8]
    thumb = hand.landmark[4]
    return math.hypot(index.x - thumb.x, index.y - thumb.y) < 0.04

# -------------------- MAIN LOOP --------------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    img = np.zeros_like(frame)
    img[:] = (20, 20, 20)  # cyber dark background

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    aim_x, aim_y = None, None
    fired = False

    # ---------- HAND ----------
    if result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

        index = hand.landmark[8]
        aim_x = int(index.x * WIDTH)
        aim_y = int(index.y * HEIGHT)

        if fire_gesture(hand) and time.time() - last_shot > 0.25:
            fired = True
            last_shot = time.time()

    # ---------- GAME OVER ----------
    if lives <= 0:
        game_over = True

    if not game_over:

        # ---------- AI DIFFICULTY ----------
        difficulty = 1 + score / 200
        spawn_rate = min(0.12, 0.03 + score / 1000)

        # ---------- SPAWN ----------
        if random.random() < spawn_rate:
            objects.append(GameObject())

        # ---------- OBJECTS ----------
        for obj in objects[:]:
            obj.move()
            obj.draw(img)

            if obj.y < -60:
                objects.remove(obj)
                lives -= 1
                combo = 1

            if fired and aim_x:
                if math.hypot(obj.x - aim_x, obj.y - aim_y) < obj.size + 25:
                    score += 10 * combo
                    combo += 1
                    last_hit_time = time.time()
                    objects.remove(obj)

                    for _ in range(25):
                        particles.append(Particle(obj.x, obj.y))

        # ---------- COMBO RESET ----------
        if time.time() - last_hit_time > 1.5:
            combo = 1

    # ---------- PARTICLES ----------
    for p in particles[:]:
        p.move()
        cv2.circle(img, (int(p.x), int(p.y)), 3, (255, 255, 255), -1)
        if p.life <= 0:
            particles.remove(p)

    # ---------- UI ----------
    if aim_x:
        cv2.circle(img, (aim_x, aim_y), 18, (0, 0, 255), 2)

    cv2.putText(img, f"Score: {score}", (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.3, (255, 255, 255), 3)

    cv2.putText(img, f"Lives: {lives}", (20, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 100, 100), 2)

    cv2.putText(img, f"Combo x{combo}", (20, 150),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 50, 50), 2)

    # ---------- CAMERA PANEL ----------
    cam_small = cv2.resize(frame, (260, 160))
    img[HEIGHT - 170:HEIGHT - 10, WIDTH - 270:WIDTH - 10] = cam_small

    # ---------- GAME OVER SCREEN ----------
    if game_over:
        cv2.putText(img, "GAME OVER", (400, 300),
                    cv2.FONT_HERSHEY_DUPLEX, 3, (255, 0, 0), 6)
        cv2.putText(img, f"Final Score: {score}", (430, 380),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 4)

    cv2.imshow("Gesture Shooter", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
