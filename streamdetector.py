import subprocess
import sys

class WindowsProcess(object):
    """
    wmic process result
    ref: https://www.denzow.me/entry/2017/09/13/235856
    """

    def __init__(self, attributes):
        """
        sample:
        caption python.exe
        commandline python  -m unittest test_OsUtil.TestOsUtils.test_01_get_processes
        creationclassname Win32_Process
        :
        writetransfercount 4800
        :param attributes:
        """
        for k, v in attributes:
            setattr(self, k.lower(), v)

    def __str__(self):
        display_name = self.commandline if self.commandline else self.caption
        return "Process[{} {} {}]".format(
            self.parentprocessid,
            self.processid,
            display_name
        )

    def get_name(self):
        return self.caption

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def get_processes():
        """
        Get process list from wmic process
        :param process_name:
        :return:
        """
        encoding = sys.stdout.encoding
        if not encoding:
            encoding = "UTF-8"
        command_str = " ".join([
            "wmic",
            "process",
            "get",
            "/FORMAT:LIST"
        ])

        result = subprocess.run(command_str, shell=True, stdout=subprocess.PIPE)
        if not result.stdout:
            return []
        process_list = []
        buf = []
        for line in result.stdout.decode(encoding).split("\r\r\n"):
            if line == "":
                if buf:
                    target_process = WindowsProcess(buf)
                    process_list.append(target_process)
                    buf = []
                continue
            key = line.split("=")[0]
            value = "=".join(line.split("=")[1:])
            buf.append([key, value])

        return process_list

    @staticmethod
    def get_process_names():
        return [p.get_name() for p in WindowsProcess.get_processes()]
  

class StreamDetector:
  def __init__(self):
    self.stream_processes = set(["obs32.exe", "obs64.exe", "obs.exe", "xsplit.core.exe", "livehime.exe", "pandatool.exe", "yymixer.exe", "douyutool.exe", "huomaotool.exe"])

  def detect(self):
    self.running_processes =set(WindowsProcess.get_process_names())
    self.detect_processes = set(self.running_processes) & self.stream_processes
    return self.detect_processes

  def is_record(self):
    process = self.detect()
    return len(process) > 0

if __name__ == '__main__':
  detector = StreamDetector()
  print('record? -> %s' % detector.is_record())