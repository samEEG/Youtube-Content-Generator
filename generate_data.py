from ExtractYoutubeComments import extract_comments
import numpy as np

print("This script generates a dataset of comments from a specific youtube channel")
print("Dataset divided respectively as: Video title, Comment, Likecount")
if __name__ == "__main__":

  channel_Id = input("Enter channel Id: ")

  #get authorization access
  youtube = extract_comments.get_authenticated_service(channel_Id)

  #search through channels uplouded videos
  #[video title, video id]
  list_of_youtube_videos = extract_comments.search_channel(youtube, channel_Id)
  dataset = []

  for item in list_of_youtube_videos:  
    #print(item)
    video_comment_threads, data_of_comment_threads = extract_comments.get_comment_threads(youtube, item)
   
    #get comments of comments 
    data_comment_of_comment = extract_comments.get_comments(youtube, video_comment_threads, item[0])
    dataset = dataset + data_of_comment_threads + data_comment_of_comment


# Save to file
  dataset = np.asarray(dataset)
  np.savetxt("foo.tsv", dataset, delimiter="\t", fmt='%s')
 
# Read from file
  
