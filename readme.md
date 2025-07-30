Index of files: 

    - dev_elm_tree.py
        Simplified version of the tree, only includes the microinverters branch, so make sure to use a microinverters diagram to test it.
        The script runs but.. It is not able to analyze the image. 
        Potential errors? 
            - The model selected 
            - The way I am uploading the image 
            - The way I am calling the image 
            - The format of the file
            - ???

    - dev_elm_tree_simplified.py
        I have cut the rest of the branch, just leaving a single interaction with the model: trying to figure out how to make the LLM actually analyze the diagram. 
        Ways that I can try this out: 
            - Try with allgit  models
            - Try with different file formats
            - Try another way to upload the file
            - Try another way to call the file

    - simple_tree_noELM.py
        Super simplified decision tree (3 branches, 2 of them are cut). 
        Send a file to the model see if it is able to open and analyze it. Works! 
        Based on the answer to the first question, it goes into severla more questions of its branch. Works accurately!  
        Initially, I was able to open and analyze it on a single interaction, but the other interactions lost track of the conversation. 
        Found the way to link interactions but it carries all the prompt from previous ones (including the image), which is token intensive. 
        For future development, think about the way to use the less number of tokens yet making it as accurate as it can be. 



Useful sources: 
    - About OpenAI's Images and Vision: https://platform.openai.com/docs/guides/images-vision?api-mode=responses