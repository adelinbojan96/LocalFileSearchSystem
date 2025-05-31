Mat generalFilter(Mat src, Mat kernel)
{
    int kr = kernel.rows;
    int kc = kernel.cols;

    float sumK, Splus = 0, Sminus = 0;
    for(int i = 0; i < kr; i++)
        for(int j = 0; j < kc; j++)
        {
            int val = kernel.at<uchar>(i, j);
            sumK += val;
            if(val > 0)
                Splus += val;
            else
                Sminus += -val;
        }

    Mat dst(src.size, CV_8U);

    for(int y = kr/2; y < src.rows - kr/2; y++)
        for(int x = kc/2; x < src.cols - kc/2; x++)
        {
            float acc = 0;
            for(int i = 0; i < kr ;i++)
            {
                yy = y + i - kr/2;
                yy = max(0, min(src.rows-1, yy));

                for(int j = 0; j < kc; j++)
                {
                    xx = x + j - kc/2;
                    xx = max(0, min(src,cols-1, xx));
                    acc += kernel.at<float>(i, j) * src.at<uchar>(yy, xx); 
                }
            }
            if(sumK > 0)
                acc /= sumK;
            else
            {
                float M = max(Splus, Sminus);
                float scale = 1/(2*M);
                float offset = 127.5f;
                acc = (acc * scale + offset);
            }

            acc = max(0, min(255, acc));
            dst.at<uchar>(y, x) = acc;
        }    
    }
    return dst;  
}

Mat medianFilter(Mat src, Mat kernel)
{

    int height = src.rows;
    int width = src.cols;
    int kr = kernel.rows;
    int kc = kernel.cols;
    int k_size = kr * kc;

    uchar nbrs[k_size];

    Mat dst(src.size(), CV_8UC1);
    long long t0 = getTickCount();
    for(int y = kr/2; height - kr/2; y++)
    {
        for(int x = kc/2; width - kc/2; x++)
        {
            int idx = 0;

            for(int i = 0; i < kr; i ++)
            {
                int yy = y + i - kr/2;
                yy = max(0, min(255, yy));

                for(int j = 0; j < kc; j++)
                {
                    int xx = x + j - kc/2;
                    xx = max(0, min(255, xx));

                    if(idx < kSize)
                        nbrs[idx++] = src.at<uchar>(yy,xx);
                }
            }
            sort(nbrs, nbrs + nbrs.size());

            uchar med = nbrs[kSize/2];
            dst.at<uchar>(y, x) = med;
        }
    }

    double t = (double) (getTickCount() - t0) / getTickFrequency();
    cout<<"Time "<< t;

    return dst;
}

Mat gaussianFilter(Mat src, Mat kernel)
{
    int kr = kernel.rows;
    int kc = kernel.cols;

    int h = src.rows;
    int w = src.cols;

    Mat dst(src.size(), src.type()); //sau CV_8UC1

    long long t0 = getTickCount();

    for(int y = 0; y < h; y++)
    {
        for(int x = 0; x < w; x++)
        {
            float sum = 0.0f;

            for(int i = 0; i < kr; i++)
            {
                int yy = y + i - kr/2;
                yy = max(0, min(255, yy));

                for(int j = 0; j < kc; j++)
                {
                    int xx = x + i - kc/2;
                    xx = max(0, min(255, xx));

                    uchar pixel = src.at<uchar>(yy, xx);
                    float weight = kernel.at<float> (i, j);

                    sum += pixel * weight;
                }
            }

            sum = max(0, min(255, sum));
            dst.at<uchar>(y, x) = sum; 
        }
    }
    return dst;
}
