import youtube_dl as ydl
import os
import scipy.io as sio


_TRAIN_SAVE_PATH_ = "..\\USAA\\train\\"
_TEST_SAVE_PATH_ = "..\\USAA\\test\\"


class MyLogger(object):
    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


ydl_opts = {
    'format': 'best[ext=mp4]',
    'logger': MyLogger(),
    'progress_hooks': [my_hook]
}


def LoadVideoID(FilePath):
    VideoIDList = []
    with open(FilePath, 'r') as FileReader:
        while True:
            ids = FileReader.readlines(100000)  # 这样读取会比一行一行读取要快，也防止了一下全部读入内存造成占用资源过多
            if not ids:
                break
            for id in ids:
                VideoIDList.append(id)
    return VideoIDList


def LoadVideoDownloadHistory(FilePath):
    DownloadHistory = []
    with open(FilePath, 'r') as FileReader:
        while True:
            lines = FileReader.readlines(100000)
            if not lines:
                break
            for l in lines:
                if l is not "\n":
                    DownloadHistory.append(l)
    return DownloadHistory


def DownloadVideo(VideoIDList, opts=ydl_opts, is_train_data=True, DownloadHistory=None):
    if is_train_data:
        ydl_opts.setdefault('outtmpl', '{}/%(id)s.mp4'.format(_TRAIN_SAVE_PATH_))
    else:
        ydl_opts.setdefault('outtmpl', '{}/%(id)s.mp4'.format(_TEST_SAVE_PATH_))

    download_list = []
    if DownloadHistory is not None:
        for i in VideoIDList:
            if i not in DownloadHistory:
                download_list.append(i)
            else:
                print("{} has already been downloaded".format(i))
    else:
        download_list = VideoIDList

    print("Total {} videos need to be downloaded".format(len(download_list)))
    downloaded_videos = []
    for id in download_list:
        url = "https://www.youtube.com/watch?v=" + id
        try:
            with ydl.YoutubeDL(opts) as downloader:
                downloader.download([url])
            downloaded_videos.append(id)
        except ydl.utils.DownloadError as dle:
            print(dle)
            print("{} cannnot be downloaded".format(id.split('\n')[0]))
            continue

    print("ALL successfully downloaded. Totally [ {} / {} ] videos have been downloaded".format(len(downloaded_videos),
                                                                                                len(download_list)))
    return downloaded_videos


if __name__ == '__main__':

    path = input("Input the path: ")
    hpath = input("Input the Download log path: ")
    is_train = bool(int(input("Use for train? [0/1]: ")))
    vlist = LoadVideoID(path)
    if hpath is not None:
        hlist = LoadVideoDownloadHistory(hpath)
    else:
        hlist = None

    dl_list = DownloadVideo(vlist, is_train_data=is_train, DownloadHistory=hlist)

    basename = os.path.basename(path).split(".")[0]
    dirPath = os.path.dirname(path) + "\\"
    log_txt = dirPath + str(basename) + "_download_log.txt"
    with open(log_txt, 'a') as FileWriter:
        for i in dl_list:
            FileWriter.write(i)

    FileWriter.close()

    """
    # TESTING
    logpath = "E:\\DATA\\GroupActivation\\USAA\\trainVidID_download_log.txt"
    path = "E:\\DATA\\GroupActivation\\USAA\\trainVidID.txt"

    VideoIDList = LoadVideoID(path)
    HistoryList = LoadVideoDownloadHistory(logpath)
    download_list = []
    if HistoryList is not None:
        for i in VideoIDList:
            if i not in HistoryList:
                download_list.append(i)
    print(len(download_list))
    print(len(VideoIDList))
    print(len(HistoryList))
    if (len(download_list) + len(HistoryList))==len(VideoIDList):
        print("YES")
    print()
    """

