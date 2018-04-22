import os
import random
from chunk import *

class LoaderRandom():
    def __init__(self, config):
        # Special frame loader that loads a randomly sample frame from any position in any video
        # until there are no frames left.

        # Create the chunks
        self.chunks = []
        print("Adding folder '%s'" % config["folder"])
        for root, dirs, files in os.walk(config["folder"]):
            for file in files:
                #print("File '%s'" % file)            
                if file.endswith(config["endswith"]):
                    #print("Adding chunk from file '%s'" % file)
                    self.chunks.append( Chunk(root, file, config["value_loader"], config["repeats"]) )
        
        # Build the set chunk+frame pairs as the load order
        self.load_sequence = []
        self.distribution = {}
        for i in range(0,len(self.chunks)):
            group = ''.join(i for i in self.chunks[i].video_filename if not i.isdigit())
            if group not in self.distribution:
                self.distribution[group] = self.chunks[i].length
            else:
                self.distribution[group] += self.chunks[i].length
            
            for j in range(0, self.chunks[i].length):
                self.load_sequence.append([i, j])
        
        # Shuffle the frame order
        random.shuffle(self.load_sequence)
        self.frame_index = 0
        print("Loaded %i frames in random loader." % len(self.load_sequence))
        print("Distribution:")
        print(self.distribution)


    def length(self):
        return len(self.load_sequence)
    
    def get_next_frame(self):
        # Get the next frame along with the data
        if self.frame_index >= len(self.load_sequence):
            return None
        
        chunk_index, index = self.load_sequence[self.frame_index]
        self.frame_index += 1
        return self.chunks[chunk_index].get_frame(index)