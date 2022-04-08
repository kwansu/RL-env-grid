# RL 그리드 환경
- 그리드 환경의 state, action, reward, transition probability을 제공.
- 주어진 그리드 환경에서 control, prediction 연습용.

<br/>

# 사용 방법
## local graphics
main.py 파일로 main loop 실행
```bash
python main.py
```
- 기본적으로 pygame으로 실시간 랜더링으로 사용.

<br/>

## google colab
- colab에서 사용시 run, main loop 없이 환경만 생성해서 사용해야함.
- 다음과 같이 환경을 생성해서 상호작용
```python
import grid_world

grid_size = (5, 6)
# colab에서는 반드시 is_render=False
env = GridWorld(grid_size, is_render=False)
```

- GridWorld의 get_image()를 통해 현재 환경이미지를 받아옴.
```python
from state import Goal
from google.colab.patches import cv2_imshow

env.change_state((0, 0), Goal))
screen_image = env.get_image()
cv2_imshow(screen_image)
```

![11](https://user-images.githubusercontent.com/15683086/162460031-0b016b2d-ac34-4040-afc0-914c531aeb11.png)


