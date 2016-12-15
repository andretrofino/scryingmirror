#include "ScryingMirror.hpp"

using namespace std;
using namespace cv;

int main(int argc, char *argv[])
{
    string img_dir = "../../../Images/Eternal Masters/";

    Mat a = imread(img_dir + "Abundant Growth.jpg");
    Mat b = imread("Abundant Growth.jpg");

    Rect art_crop = Rect(Point(18, 36), Point(204, 172));

    Mat art = a(art_crop);

    Hash hash = dct_hash(art);

    // hash_dir(img_dir, "../../ema_dct.phash");

    vector<pair<string, Hash>> hash_values = load_hash("../../../ema_dct.phash");

    vector<pair<string, int>> scores = match(hash, hash_values);

	return 0;
}