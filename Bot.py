import telebot
from telebot import types
from pytube import YouTube
from moviepy.editor import VideoFileClip
import os

bot = telebot.TeleBot('6376347293:AAHKkjC5kaMJmuQpjrPhjDxUdF7Cb0rRO9I')

user_states = {}
links=[]
@bot.message_handler(commands=['start', 'help'])
def start(message):
        
        keyboard = types.InlineKeyboardMarkup(); 
       
        key_download_video = types.InlineKeyboardButton(text='Download Video', callback_data='Download_Video')
        key_video_to_audio = types.InlineKeyboardButton(text='Convert Video to Audio', callback_data='Convert_Video_to_Audio')
        
        keyboard.add(key_video_to_audio, key_download_video)

        bot.send_message(message.chat.id, "Hello! I'm a bot that can manage your youtube account. Pick an option.", reply_markup=keyboard)



@bot.callback_query_handler(func=lambda call: True)
def handle_options_button(call):
        user_id = call.from_user.id
        if call.data == 'Download_Video':
               user_states[user_id] = 'download_video'
               bot.send_message(call.message.chat.id, "Send a link")        
        elif call.data == 'Convert_Video_to_Audio':
                user_states[user_id] = 'convert_video_to_audio'
                bot.send_message(call.message.chat.id, "Send a youtube video link and how you'd like to name audio file: 'link, file name'")
        elif call.data == '360p':
              get_video(links.pop(),call.message.chat.id, '360p')
        elif call.data == '720p':
              get_video(links.pop(),call.message.chat.id, '720p')
        elif call.data == '1080p':
              get_video(links.pop(),call.message.chat.id, '1080p')
        elif call.data == '480p':
              get_video(links.pop(),call.message.chat.id, '480p')
        elif call.data == '240p':
              get_video(links.pop(),call.message.chat.id, '240p')    
        elif call.data == '1440p':
              get_video(links.pop(),call.message.chat.id, '1440p') 
        elif call.data == '2160p':
              get_video(links.pop(),call.message.chat.id, '2160p') 


@bot.message_handler(func=lambda message: message.from_user.id in user_states)
def handle_user_response(message):
    user_id = message.from_user.id
    state = user_states.pop(user_id)  
    if state == 'download_video':
        links.append(message.text)
        get_quality(message)
    elif state == 'convert_video_to_audio':
        get_vid_toAud(message)
  




def get_video(Url,chat_id, desired_quality):
        try:  
            yt = YouTube(Url)

            video_streams = yt.streams.all()
            
            selected_stream = None
            for stream in video_streams:
                  if stream.resolution == desired_quality:
                        selected_stream = stream
                        break

            if selected_stream:
                video_path = '\\videos'
                selected_stream.download(video_path)

                video_file = open(f'{video_path}\\{selected_stream.default_filename}', 'rb')
                bot.send_chat_action(chat_id, 'upload_video')
                bot.send_video(chat_id, video_file)
            else:
                  bot.send_message(chat_id, "Desired quality not found:(")
                
        except Exception as e:
            bot.send_message(chat_id, f'Oops! An error occured! {e}')

def get_quality(message):
        keyboard = types.InlineKeyboardMarkup(); 

        key_720 = types.InlineKeyboardButton(text='720p', callback_data='720p')
        key_360 = types.InlineKeyboardButton(text='360p', callback_data='360p')
        key_1080 = types.InlineKeyboardButton(text='1080p', callback_data='1080p')
        key_480 = types.InlineKeyboardButton(text='480p', callback_data='480p')
        key_240 = types.InlineKeyboardButton(text='240p', callback_data='240p')
        key_1440 = types.InlineKeyboardButton(text='1440p', callback_data='1440p')
        key_2160 = types.InlineKeyboardButton(text='2160p', callback_data='2160p')

        keyboard.add(key_720, key_360, key_240, key_480, key_1080, key_1440, key_2160)
        bot.send_message(message.chat.id, "Pick quality", reply_markup=keyboard)
        


def get_vid_toAud(message):
        try:
            url = message.text.split(", ")[0]
            yt = YouTube(url)
            bot.send_message(message.from_user.id, "Getting the video...")
            stream = yt.streams.filter(file_extension='mp4').first()
            video_path = stream.download("\\videos")
            
            
            output_dir = 'audios'
            os.makedirs(output_dir, exist_ok=True)

            video = VideoFileClip(video_path)

            
            audio_path = os.path.join(output_dir, message.text.split(", ")[1])

            video.audio.write_audiofile(f'{audio_path}.mp3', codec='libmp3lame')

            bot.send_chat_action(message.chat.id, 'upload_audio')

            audio_file = open(f'{audio_path}.mp3', 'rb')
            bot.send_audio(message.chat.id, audio_file)

            video.close()

        except Exception as e:
            bot.reply_to(message, f'Oops! An error occured! {e}')


bot.polling(non_stop=True)