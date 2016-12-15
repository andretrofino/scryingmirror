
#include "ImageHash.hpp"

using namespace std;
using namespace cv;

vector<double> dct(const vector<double> &x)
{
    size_t N = x.size();

    vector<double> y(N);

    double div = 2 * (double)N;

    for (int k = 0; k < N; ++k) {
        double pi_k = M_PI * k;
        for (int n = 0; n < N; ++n) {
            y[k] += x[n] * cos(pi_k * (2 * n + 1) / div);
        }
        y[k] *= 2;
    }

    return y;
}

double median(const Mat &x)
{
    int w = x.cols;
    int h = x.rows;

    Mat y;
    x.reshape(0, 1).copyTo(y);

    int size = y.cols;

    cv::sort(y, y, SORT_ASCENDING);

    double median;
    if (size % 2 == 0) {
        median = (y.at<float>(0, size / 2 - 1) + y.at<float>(0, size / 2)) / 2;
    } else {
        median = y.at<float>(0, size / 2);
    }

    return median;
}

Hash calcHash(const Mat &x, double median)
{
    const float *x_ptr = x.ptr<float>();

    int size = x.cols * x.rows;

    vector<bool> hash_vector(size);

    for (int i = 0; i < size; ++i) {
        if (*x_ptr > median) {
            hash_vector[i] = true;
        }
        x_ptr++;
    }

    return Hash(hash_vector);

}

Mat dct(const Mat &img)
{
    int w = img.cols;
    int h = img.rows;

    const uchar *ptr_start = img.ptr();

    Mat dct_img(h, w, CV_32F);
    float *dct_ptr = dct_img.ptr<float>();

    // Horizontal DCT
    for (int y = 0; y < h; ++y) {
        const uchar *ptr_end = ptr_start + w;
        vector<double> row(ptr_start, ptr_end);

        vector<double> dct_row = dct(row);

        Mat tmp(dct_row);
        tmp = tmp.t();
        tmp.row(0).copyTo(dct_img.row(y));

        ptr_start += w;
    }

    // Vertical DCT
    for (int x = 0; x < w; ++x) {
        Mat mat_col = dct_img.col(x).t();
        vector<double> col(h);
        mat_col.copyTo(col);

        vector<double> dct_col = dct(col);

        Mat tmp(dct_col);
        tmp.col(0).copyTo(dct_img.col(x));
    }

    return dct_img;
}

Hash dct_hash(const Mat &input, int rsz, int block_size, bool crop)
{
    Mat img;

    if (crop) {
        Rect crop_rect = Rect(Point(18, 36), Point(204, 172));
        input(crop_rect).copyTo(img);
    } else {
        input.copyTo(img);
    }

    if (img.channels() == 3) {
        cvtColor(img, img, CV_BGR2GRAY);
    }

    resize(img, img, Size(rsz, rsz));

    Mat dct_img = dct(img);
    Rect lowfreq_rect(0, 0, block_size, block_size);

    Mat lowfreq_dct;
    dct_img(lowfreq_rect).copyTo(lowfreq_dct);

    double med = median(lowfreq_dct);

    Hash h = calcHash(lowfreq_dct, med);

    return h;
}

void hash_dir(const string dir, const string filename)
{
    vector<String> image_files;
    image_files.reserve(250);

    string pattern = dir;
    if (pattern[pattern.size() - 1] != '/') {
        pattern += '/';
    }
    pattern += "*.jpg";

    glob(pattern, image_files);

    ofstream hash_file(filename);

    for (String s : image_files) {
        Mat img = imread(s);
        Hash h = dct_hash(img, 32, 8, true);
        // Get Card name
        string card_name = s.substr(s.find("\\") + 1);
        // Remove .jpg extension
        card_name = card_name.erase(card_name.find('.'), 4);

        hash_file << card_name << ":" << h.hash_value << endl;

    }
    
    hash_file.close();
}

vector<pair<string, Hash>> load_hash(string hash_path)
{
    vector<pair<string, Hash>> hash_values;
    ifstream hash_file(hash_path);

    string line;
    while (getline(hash_file, line)) {
        string name;
        string hash;
        pair<string, Hash> pair("", 0);

        size_t index = line.find(":");

        name = line.substr(0, index);
        hash = line.substr(index + 1);

        pair.first = name;
        pair.second = Hash(stoul(hash));

        hash_values.push_back(pair);
    }

    return hash_values;
}

vector<pair<string, int>> match(Hash target_hash, vector<pair<string, Hash>> &hash_list, int top)
{
    size_t N = hash_list.size();
    vector<pair<string, int>> scores(N);

    for (int i = 0; i < N; ++i)  {
        scores[i].first = hash_list[i].first;
        scores[i].second = hash_list[i].second - target_hash;
    }
    
    sort(scores.begin(), scores.end(), [](const std::pair<string, int> &left, const std::pair<string, int> &right) {
        return left.second < right.second;
    });

    vector<pair<string, int>> top_scores(scores.begin(), scores.begin() + top);
    return top_scores;
}