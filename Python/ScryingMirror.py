import MTGHash
import cv2
from imagehash import *
from CardFinder import *

def main():
    width = 187
    height = 137

    str_hash_list, name_list = MTGHash.load_hash('ema_ogw_dct_avg.hash')
    hash_list = [hex_to_hash(value) for value in str_hash_list]

    try:
        cap = cv2.VideoCapture(0)

        screen_width = cap.get(3)
        screen_height = cap.get(4)

        x = int(screen_width / 2 - width / 2)
        y = int(screen_height / 2 - height / 2)

        last_result = ''

        # cap.set(13, 0)
        # cap.set(14, 0)
        while cap.isOpened():
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)

            roi = frame[y:y + height, x:x + width]

            roi_hash = MTGHash.dct_hash(cv2.flip(roi, 1), crop=False)

            scores, index_list = MTGHash.match(roi_hash, hash_list)

            total_diff = 0

            for i in xrange(1, 5):
                total_diff += scores[i] - scores[i - 1]

            if total_diff > 5:

                if last_result != name_list[index_list[0]]:

                    cv2.imshow("Roi", roi)

                    for score, index in zip(scores, index_list):
                        print name_list[index] + ' : ' + str(score)
                    print '\n'

                    last_result = name_list[index_list[0]]

            cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 0, 255))

            cv2.imshow('Frame', frame)

            key = cv2.waitKey(1)

            if key & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


def find_card_main():
    str_hash_list, name_list = MTGHash.load_hash('ema_ogw_dct_avg.hash')
    hash_list = [hex_to_hash(value) for value in str_hash_list]

    try:
        cap = cv2.VideoCapture(0)

        screen_width = cap.get(3)
        screen_height = cap.get(4)

        last_result = ''

        # cap.set(13, 0)
        # cap.set(14, 0)
        while cap.isOpened():
            ret, frame = cap.read()
            # frame = cv2.flip(frame, 1)

            roi = find_card(frame)

            if roi is not None:
                cv2.imshow('Art Crop', roi)

                roi_hash = MTGHash.dct_hash(cv2.flip(roi, 1), crop=False)

                scores, index_list = MTGHash.match(roi_hash, hash_list)

                total_diff = 0

                for i in xrange(1, 5):
                    total_diff += scores[i] - scores[i - 1]

                if total_diff > 5:

                    if last_result != name_list[index_list[0]]:

                        for score, index in zip(scores, index_list):
                            print name_list[index] + ' : ' + str(score)
                        print '\n'

                        last_result = name_list[index_list[0]]

            cv2.imshow('Frame', frame)

            key = cv2.waitKey(1)

            if key & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
