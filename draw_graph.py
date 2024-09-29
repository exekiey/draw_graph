from PIL import Image, ImageDraw, ImageFont
import math


def draw_ellipse(draw, center, radii, fill):
    
    x, y = center
    rx, ry = radii
    
    bounding_box = [x - rx, y - ry, x + rx, y + ry]
    draw.ellipse(bounding_box, fill=fill)

def draw_centered_text(draw, position, text, font, fill):
    
    x, y = position
    bbox = font.getbbox(text)
    
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    text_x = x - (text_width / 2)
    text_y = y - (text_height / 2)
    
    draw.text((text_x, text_y), text, fill=fill, font=font)



def draw_graph(nodes_matrix, number_of_nodes):


    width = 1000
    height = 1000

    image = Image.new('RGB', (width, height), 'white')

    draw = ImageDraw.Draw(image)

    center_x = width / 2
    center_y = height / 2

    radius = min(center_x, center_y) * 0.9

    font = ImageFont.truetype("arial.ttf", 50)
    cost_font = ImageFont.truetype("arial.ttf", 25)

    line_poses = []
    text_poses = []

    for i, row in enumerate(nodes_matrix):

        angle = (i * (1 / number_of_nodes)) * (math.pi * 2)
        x = math.cos(angle) * radius
        y = math.sin(angle) * radius

        x_pos = center_x + x
        y_pos = center_y + y

        draw_ellipse(draw, (x_pos, y_pos), (50, 50), fill = 'blue')
        draw_centered_text(draw, (x_pos, y_pos), text = str(i+ 1), fill = 'black', font = font)

        for j in range(i, number_of_nodes):

            cost = row[j]

            if cost == -1 or j == i:
                continue


            other_angle = (j * (1 / number_of_nodes)) * (math.pi * 2)
            other_x = math.cos(other_angle) * radius
            other_y = math.sin(other_angle) * radius

            direction = (other_x - x, other_y - y)

            module = math.sqrt(direction[0] * direction[0] + (direction[1] * direction[1]))

            normal_direction = (direction[0] / module, direction[1] / module)

            increase_direction = module * 0.1

            text_pos = (normal_direction[0] * increase_direction + x_pos, normal_direction[1] * increase_direction + y_pos)
            

            draw.line([(x_pos, y_pos), (center_x + other_x, center_y + other_y)], fill = 'red', width = 5)
            
            line_poses.append(((x_pos, y_pos), (center_x + other_x, center_y + other_y)))
            text_poses.append((text_pos, cost))

    for i in line_poses:
        draw.line([i[0], i[1]], width=5, fill = 'red')


    counter = 0
    for i in text_poses:
        


        draw_ellipse(draw, i[0], (15, 15), (255, 255, 255, 125 ))
        draw_centered_text(draw, position = i[0], text = str(i[1]), fill = 'green', font = cost_font)
        
        counter += 1


    image.show()
