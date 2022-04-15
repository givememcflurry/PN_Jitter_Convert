from PIL import Image
import math


# 측정결과 자름
def cut(input_file):
    input_image = Image.open(input_file)
    cut_image = input_image.crop((66, 171, 509, 430))  # 433*259
    name = 'cut ' + input_file
    cut_image.save(name)


# ★이미지를 RGB로 변환
def rgb(input_image):
    image_size = input_image.size
    rgb_image = Image.new('RGB', (image_size[0], image_size[1]))
    rgb_image.paste(input_image, (0, 0))
    return rgb_image


# 결과확대사진 그래프화
def gra(input_file, plot_file):
    graph = Image.new('RGB', (1400, 1100))
    input_image = Image.open(input_file)
    plot_image = Image.open(plot_file)
    graph.paste(plot_image, (0, 0))
    graph.paste(input_image, (120, 0))
    name = 'plot ' + input_file
    graph.save(name)


# 측정결과 확대 및 가로 세로축 입력
def plot(input_file):
    input_image = Image.open(input_file)  # 측정결과 호출
    cut_image = input_image.crop((66, 171, 509, 429))  # 결과사진 자름
    enlarged_image = cut_image.resize((1280, 960))  # 자른사진 확대
    graph = Image.new('RGB', (1400, 1100))  # 오프셋 이미지 생성
    plot_image = Image.open('plot.png')  # 플롯이미지 호출
    graph.paste(plot_image, (0, 0))  # 오프셋에 플롯 붙임
    graph.paste(enlarged_image, (120, 0))  # 플롯에 확대사진 붙임
    name = 'plot ' + input_file  # 저장할 파일의 이름 설정
    graph.save(name)  # 수정한 이미지저장


# 측정결과 그래프 추출
def ext(input_file):
    input_image = Image.open(input_file)  # 측정결과 호출
    cut_image = input_image.crop((66, 171, 509, 430))  # 결과사진 자름

    rgb_image = Image.new('RGB', (433, 259))
    rgb_image.paste(cut_image, (0, 0))
    ext_image = Image.new('RGB', (433, 259), (255, 255, 255))

    hp, vp = 0, 0
    while hp < 433:
        while vp < 259:
            ri_r, ri_g, ri_b = rgb_image.getpixel((hp, vp))
            if (ri_r < 5 and ri_g > 240 and ri_b > 240):
                ext_image.putpixel((hp, vp), (0, 0, 0))
            vp = vp + 1
        hp = hp + 1
        vp = 0

    name = 'ext ' + input_file
    ext_image.save(name)


# 그래프 격자 추출
def crs(input_file):
    input_image = Image.open(input_file)  # 측정결과 호출
    cut_image = input_image.crop((66, 171, 509, 430))  # 결과사진 자름

    rgb_image = Image.new('RGB', (433, 259))
    rgb_image.paste(cut_image, (0, 0))
    ext_image = Image.new('RGB', (433, 259), (255, 255, 255))

    hp, vp = 0, 0
    while hp < 433:
        while vp < 259:
            ri_r, ri_g, ri_b = rgb_image.getpixel((hp, vp))
            if (ri_r == 112 and ri_g == 112 and ri_b == 112):
                ext_image.putpixel((hp, vp), (0, 0, 0))
            vp = vp + 1
        hp = hp + 1
        vp = 0

    ext_image.save('graph cross.png')


# 픽셀위치 추출
def pix(input_file):
    input_image = Image.open(input_file)
    rgb_image = rgb(input_image)

    hp, vp = 0, 0
    while hp < 433:
        while vp < 259:
            ri_r, ri_g, ri_b = rgb_image.getpixel((hp, vp))
            if (ri_r == 0 and ri_g == 0 and ri_b == 0):
                print(hp, vp)
                vp = 258
            vp = vp + 1
        hp = hp + 1
        vp = 0


# ★지터계산(MATLAB)을 위한 그래프 값 추출(Sampling)
def smp(input_file):
    input_image = Image.open(input_file)  # 측정결과 호출
    cut_image = input_image.crop((66, 171, 507, 429))  # 결과이미지 자름(L,U,R,D)
    rgb_image = rgb(cut_image)  # 자른이미지를 RGB로 변환
    image_size = rgb_image.size  # (hp_max, vp_max) = (443, 259)
    hp_max = image_size[0]  # 변환이미지의 최대 horizon-pixel
    vp_max = image_size[1]  # 변환이미지의 최대 vertical-pixel

    freq_min = 500  # 최소 주파수 (입력)
    freq_max = 50000000  # 최대 주파수 (입력)
    deci_min = -40  # 최소 데시벨 - 절대값상 최소 (입력)
    deci_max = -140  # 최대 데시벨 - 절대값상 최대 (입력)

    hp, vp = 0, 0  # 가로, 세로
    freq_list = []  # freq 리스트
    deci_list = []  # deci 리스트

    while hp < hp_max:
        while vp < vp_max:
            ri_r, ri_g, ri_b = rgb_image.getpixel((hp, vp))  # 픽셀의 RGB값 추출
            if (ri_r < 5 and ri_g > 240 and ri_b > 240):  # 그래프 색깔 조건

                fr_sample = (freq_max / freq_min) ** (1 / hp_max)  # pixel -> freq 변환 (ex. 500Hz ~ 50MHz)
                db_sample = (deci_max - deci_min) / vp_max  # pixel -> deci (ex. -40dB ~ -140dB)

                fr_value = round(freq_min * (fr_sample ** hp))  # freq 소수자리 반올림
                db_value = round(deci_min + (db_sample * vp))  # deci 소수자리 반올림

                freq_list.append(fr_value)  # freq 리스트에 hp_value를 추가
                deci_list.append(db_value)  # deci 리스트에 vp_value를 추가

                vp = vp_max - 1  # 다음 hp로 넘어가기 위한 vp 입력
            vp = vp + 1
        hp = hp + 1
        vp = 0

    return freq_list, deci_list


# ★시그마 안의 값 개별 계산
def cal(b1, b2, f1, f2):
    a1 = (b2 - b1)/(math.log10(f2) - math.log10(f1))
    res = ((10 ** (b1 / 10)) * (f1 ** (-a1 / 10)) * ((a1 / 10 + 1) ** (-1))
           * ((f2 ** (a1 / 10 + 1)) - (f1 ** (a1 / 10 + 1))))
    return res


# MATLAB 계산용 추출
def mat(input_file):
    frq = smp(input_file)[0]
    dbc = smp(input_file)[1]
    print(frq, dbc)


# [Final]측정이미지 지터값으로 변환 22.04.15
def pjc(input_file):
    frq = smp(input_file)[0]
    dbc = smp(input_file)[1]
    fc = 1.0e+9  # 반송주파수(값입력)
    cnt = 0
    cal_list = []

    while cnt < len(frq)-1:
        cal_list.append(cal(dbc[cnt], dbc[cnt+1], frq[cnt], frq[cnt+1]))
        cnt += 1

    sum_cal = sum(cal_list)
    jitter = ((2 * sum_cal) ** (0.5)) / (2 * 3.141592 * fc)

    print("RMS Jitter =", jitter)
