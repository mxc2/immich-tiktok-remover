# Immich-Tiktok-Remover - Get rid of those annoying TikTok videos
Immich-Tiktok-Remover is a tool focused on automatically removing TikTok videos from your self-hosted Immich. Uses EasyOCR and offers high customizability, allowing to delete even more than just TikTok videos.

## Why?
Despite having approximately 1.2 billion active users per month, TikTok still does not allow users to change the default download location for TikTok videos. This means that these videos are typically saved in the DCIM folder, mixing with photos taken with the camera. This causes TikTok videos to be added to the Memories section in Immich, and overall just degrading the average experience because precious photos are mixed with random videos intended for sharing with friends.

## How it works
Utilizing the Immich API, immich-tiktok-remover checks every uploaded video against a number of requirements (file type, file name length, file name style and file creation date) and if it passes those requirements, then the video is sent trough EasyOCR and checked for a TikTok watermark. If a watermark is found, then said video gets trashed or archived, based on to the user's preferance.

## How good is it?
In my testing, out of 3569 videos, Immich-Tiktok-Remover found 1953 TikTok videos. After manually going through all my videos, I found that 8 videos were falsely not detected as TikTok. This was mainly caused by the watermark being covered by white text or two TikTok watermarks being on top of each other.

1953 videos correctly detected out of 1961 makes it a 99.5% success rate.

I found no videos that were falsely detected as TikToks.

## Usage

Getting this script to run is as easy as one-two-three:

1. **Check Python and pip Installation:** Ensure that Python and pip are installed on your system.
2. **Download and Navigate:** Download the project and navigate to its directory using your terminal.
3. **Install Dependencies:** Install the necessary dependencies by executing `pip install -r requirements.txt`.
4. **Run the Script:** Once dependencies are installed, execute the script using `python ./src/immich_tiktok_remover.py`. You can add parameters to the end of that line f.e. `python ./src/immich_tiktok_remover.py --archive`

### Why no simple download in Releases section? 
EasyOCR uses a dependency called torch, which is a really big package. The size of the package sadly crosses the maximum file size of Github releases.

## Customization
Here are all the customization options available for Immich-Tiktok-Remover:

| Command | Description | Type | Default
| --- | --- | --- | --- |
| `--output-all` | Outputs every file name that has been checked in EasyOCR. | Boolean | False |
| `--archive` | Rather than trashing every TikTok video that has been found, this parameter archives found videos. | Boolean | False |
| `--search-archived` | By default, immich-tiktok-remover searches only for videos that have not been archived. This parameter overrides this. Note: This disables `-archive` parameter | Boolean | False |
| `--file-types` | By default, immich-tiktok-remover searches only for .mp4 videos. Use this to specify file types for the tool to search for. For example, `--file-types mp4,mov` would search for both .mp4 and .mov files. Setting this to 0, disables this requirement. | List | mp4 |
| `--file-name-length` | Set the length, that the video file name needs to be (without file extension), for it to be considered a potential TikTok video. Setting this to 0, disables this requirement. | int | 32 |
| `--file-name-is-not-alumn` | By default, video files that include only alphanumeric characters are considered potential TikTok videos. This parameter overrides that requirement. | Boolean | False |
| `--file-created-after` | Videos created before September 2016 are ignored. Use this parameter to adjust the timestamp. Note: This parameter only accepts Epoch timestamps. Setting this to 0, disables this requirement. | int | 1472688000 |
| `--text-to-check` | By default, EasyOCR checks for "TikTok" text in the video. You can change this by using this parameter, i.e. setting this to "Google" searches for text "Google" in videos. If EasyOCR finds the requested text, then that video is trashed/archived | String | TikTok |

### How to use customization parameters
**Boolean parameters:**

```bash
./immich-tiktok-remover --archive --file-name-is-not-alum
```
Passes the archive and file-name-is-not-alum parameter

**Int and String parameters**

```bash
./immich-tiktok-remover --file-created-after 1502688000 --text-to-check Instagram
```
Sets the --file-created-after to 1502688000 (2019 November 2) and --text-to-check to Instagram

**List parameters**

```bash
./immich-tiktok-remover --file-types mp4,webp,mov
```
Sets the --file-types to check mp4, webp and mov files.

## What Immich-Tiktok-Remover can't do
- It cannot by itself delete TikTok videos as soon as you upload one. Immich-Tiktok-Remover only removes TikTok videos when you either manually run it or schedule its execution, for example, by creating a cron job.
- Immich-Tiktok-Remover can't remove all TikTok videos in a few seconds. This is a process that can take some time, simply because of the way EasyOCR works and the performance it can deliver.
- Currently, Immich-Tiktok-Remover only works with videos. Images, downloaded from TikTok, aren't currently automatically deleted from Immich.

## Thanks
Big thanks for the Immich team for building such a great project.
