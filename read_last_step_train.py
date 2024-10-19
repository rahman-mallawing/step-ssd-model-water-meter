import tensorflow as tf
import os
import random

def get_last_step(log_dir='/content/training/train'):
    # Memastikan ada event files di dalam direktori log
    event_files = [os.path.join(log_dir, file) for file in os.listdir(log_dir) if file.startswith('events')]

    if not event_files:
        print("No event files found.")
        return random.randint(0, 1000)  # Mengembalikan nilai random jika tidak ada event file
    
    print(f"Found {len(event_files)} event files.")
    
    # Variabel untuk menyimpan step dan loss terakhir
    last_step = None
    last_total_loss = None

    # Iterasi melalui setiap event file
    for event_file in event_files:
        print(f"Processing event file: {event_file}")

        # Membaca event file dengan TFRecordDataset
        dataset = tf.data.TFRecordDataset(event_file)

        for raw_record in dataset:
            # Decode Summary Log Event
            event = tf.compat.v1.Event.FromString(raw_record.numpy())
            for value in event.summary.value:
                if value.tag == 'Loss/total_loss':  # Ganti dengan tag yang sesuai
                    last_step = event.step
                    last_total_loss = value.simple_value

    # Mengembalikan step terakhir atau nilai random jika step tidak ditemukan
    if last_step is not None:
        return last_step
    else:
        print("No 'Loss/total_loss' found.")
        return random.randint(0, 1000)  # Mengembalikan nilai random jika tidak ada loss yang ditemukan
