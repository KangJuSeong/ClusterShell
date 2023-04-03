# CLSH
20181569 소프트웨어학부 강주성

## CLSH 설계
- 옵션 1
	- —hostfile 옵션이 없을 경우 기존에 컨테이너를 빌드하면서 작성했던 환경변수 CLSH_ HOSTS와 CLSH_ HOSTFILE 의 값을 가져오게 됩니다.
	- 위에 해당하는 환경변수가 없을 경우 현재 작업 디렉토리에서 hostfile을 찾아서 가져오게 됩니다.
	- 환경변수와 hostfile 모두 존재하지 않으면 종료됩니다.
- 옵션 2
	- —out 으로 경로가 들어왔을 때 경로에 해당 node.out 파일을 생성하고 표준 입출력을 해당 파일로 연결하여 출력 결과를 작성합니다.

## CLSH 구현
### 기본 구현
- Docker 를 이용하여 하나의 호스트에서 다수의 컨테이너로 명령어를 보내서 결과를 가져오는 구조입니다.
- 컨테이너와의 통신은 하나의 볼륨을 마운팅하고 해당 볼륨에 양방향 FIFO를 만들어서 구현하였습니다.
- 언어는 python 을 이용하였고 CLI 형식의 구현을 위한 click 모듈을 사용하여 구현했습니다.
- `clsh.py`는 입력 받은 명령어를 FIFO 를 통해 `node.py`로 보내며 명령어를 받은 `node.py`는 해당 명령에 대한 수행을 서브 프로세스를 생성하여 작업하고 해당 결과를 반환해주며 반환된 결과를 FIFO 를 이용하여 `clsh.py`로 반환해주는 역할을 합니다.
- 반환된 결과는 각 node 별 결과가 테이블에 출력되도록 작성하였습니다.
### 선택한 옵션
- 옵션1
	- —hostfile 이라는 옵션을 통해 hostfile의 경로를 입력 받아 해당 파일에 있는 node의 값들을 가져와서 명령어들을 해당 node로 보내주게 되는데 여기서 —hostfile 옵션이 주어지지 않았다면 기존에 dockerfile에 정의했던 환경변수 중 CLSH_HOSTS 의 값을 `os.getenv()`를 이용하여 먼저 가져오게 됩니다. 여기서 CLSH_HOSTS의 값은 콜론을 기준으로 하여 node를 읽어와서 명령을 수행하게 됩니다.
	- 만약에 CLSH_HOSTS 값이 존재하지 않는다면 다음에는 CLSH _HOSTFILE 의 값을 가져오게 되는데 해당 환경변수에는 hostfile의 상대경로 또는 절대 경로가 있고 해당 값을 읽어와서 파일을 열고 node 값을 가져와 명령을 수행하게 됩니다.
	- 두가지 환경변수가 모두 존재하지 않는다면 현재 디렉토리에서 hostfile을 읽어서 명령을 수행하게 됩니다.
	- hotfile도 존재하지 않는다면 메시지 출력 후 종료하게 됩니다.
- 옵션2
	- —out 옵션을 통해 경로가 주어지면 해당 경로에 node.out 이라는 파일을 만들고 해당 파일에 명령 수행 결과를 입력합니다.
	- —out 옵션이 주어지지 않았을 때는 위 작업이 이루어지면 안되기 때문에 이때는 명령에 대한 결과를 명령을 수행했던 node에서 콘솔로 출력하게 됩니다.

## CLSH 결과
### Install
- Docker를 이용하여 host와 node를 구현하였으므로 docker-compose를 이용하여 build 해야 합니다.
- `docker-compose up --d --build` -> node1, node2, node3, nod4, host 컨테이너 모두 실행
- `docker ps` -> 위 다섯개 컨테이너가 출력되면 준비가 끝났습니다.
![](./readme_img/clash_1.png)
- `docker exec -it host /bin/bash` -> 클러스터쉘을 이용하기 위한 host 컨테이너에 들어갑니다.
![](./readme_img/clash_2.png)

### Execute
- `clsh -h node1 cat /proc/loadavg` -> node1에 명령어 실행해보기
![](./readme_img/clash_3.png)
- `clsh -h node1,node2,node3,node4 cat /proc/loadavg` -> 네개의 node에 명령어 실행해보
![](./readme_img/clash_4png)

### Method
- `clsh --hostfile ./hostfile cat /proc/loadavg` -> 해당 명령어를 통해 hostfile에 있는 node로 명령어 실행해보기
![](./readme_img/clash_5.png)
- 다른 호스트파일인 test 파일을 넣어서 재실행 -> test 에는 node1 과 node3 만 존재
![](./readme_img/clash_6.png)
- —hostfile 이 생략되고 환경변수 CLSH_HOSTS 가 존재할 때
![](./readme_img/clash_7.png)
![](./readme_img/clash_8.png)
- —hostfile 이 생략되고 환경변수 CLSH_HOSTFILE 이 존재할 때
![](./readme_img/clash_9.png)
![](./readme_img/clash_10.png)
- 환경변수가 모두 존재하지 않을 때
![](./readme_img/clash_11.png)
- 환경변수와 호스트파일 모두 존재하지 않을 때
![](./readme_img/clash_12.png)

- `clsh —out /app -h node1 cat /proc/loadavg` -> /app 디렉토리에 node1.out 파일을 생성하고 해당 파일에 결과 입력
![](./readme_img/clash_13.png)
![](./readme_img/clash_14.png)
-> 네개의 노드 모두 출력 파일 생성
