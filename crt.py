import moderngl
import pygame

CRT_VERT = '''
    #version 330 core

    uniform vec2 offset;
    uniform vec2 scale;

    vec2 vertices[3] = vec2[](
        vec2(-1.0, -1.0),
        vec2(3.0, -1.0),
        vec2(-1.0, 3.0)
    );

    out vec2 vertex;

    void main() {
        gl_Position = vec4(vertices[gl_VertexID], 0.0, 1.0);
        vertex = (vertices[gl_VertexID] + offset) * scale;
    }
'''

CRT_FRAG = '''
    #version 330 core

    uniform float color_shift;
    uniform int color_mode;
    uniform int enable_noise;
    uniform int enable_scanline;
    uniform int enable_multisample;
    uniform int enable_screen;

    uniform float time;
    uniform vec2 screen_size;
    uniform sampler2D Texture;

    in vec2 vertex;
    layout (location = 0) out vec4 out_color;

    float hash13(vec3 p3) {
        p3 = fract(p3 * 0.1031);
        p3 += dot(p3, p3.zyx + 31.32);
        return fract((p3.x + p3.y) * p3.z);
    }

    vec2 hash23(vec3 p3) {
        p3 = fract(p3 * vec3(0.1031, 0.1030, 0.0973));
        p3 += dot(p3, p3.yzx + 33.33);
        return fract((p3.xx + p3.yz) * p3.zy);
    }

    vec3 aces(vec3 x) {
        const float a = 2.51;
        const float b = 0.03;
        const float c = 2.43;
        const float d = 0.59;
        const float e = 0.14;
        return clamp((x * (a * x + b)) / (x * (c * x + d) + e), 0.0, 1.0);
    }

    vec3 sample_screen(vec2 uv) {
        if (color_shift == 0.0) {
            return texture(Texture, uv).rgb;
        }
        return vec3(
            texture(Texture, uv - color_shift).r,
            texture(Texture, uv).g,
            texture(Texture, uv + color_shift).b
        );
    }

    vec3 screen(vec2 vertex) {
        if (abs(vertex.x) > 1.001 || abs(vertex.y) > 1.001) {
            return vec3(0.0);
        }
        vec2 uv = vertex * 0.5 + 0.5;
        uv.y = 1.0 - uv.y;
        vec3 color = sample_screen(uv);
        if (enable_noise == 1) {
            float noise = hash13(floor(vec3(uv * screen_size, floor(time))));
            color *= 1.0 + (noise - 0.5) * 0.1;
        }
        if (enable_scanline == 1) {
            float scanline = sin(uv.y * screen_size.y * 3.141592 + time * 0.05) * 0.1 + 0.9;
            color *= scanline;
        }
        if (color_mode == 1) {
            color = color * 1.05 + 0.05;
        }
        if (color_mode == 2) {
            color = aces(color);
        }
        return color;
    }

    void main() {
        if (enable_screen == 0) {
            if (abs(vertex.x) <= 1.0 || abs(vertex.y) <= 1.0) {
                vec2 uv = vertex * 0.5 + 0.5;
                uv.y = 1.0 - uv.y;
                out_color = texture(Texture, uv).rgba;
            } else {
                out_color = vec4(0.0, 0.0, 0.0, 1.0);
            }
            return;
        }
        vec2 v = vertex * (1.0 + pow(abs(vertex.yx), vec2(2.0)) * 0.1);
        vec3 color = vec3(0.0);
        if (enable_multisample == 1) {
            for (int i = 0; i < 16; ++i) {
                vec2 offset = hash23(vec3(v * screen_size, float(i))) - 0.5;
                color += screen(v * 1.01 + offset / screen_size);
            }
            color /= 16.0;
        } else {
            color = screen(v * 1.01);
        }
        out_color = vec4(color, 1.0);
    }
'''


class CRT:
    def __init__(self, render_size, window_size):
        self.ctx = moderngl.get_context()
        self.ctx.screen.size = window_size
        self.texture = self.ctx.texture(render_size, 'rgba8unorm')
        self.ctx.shaders['crt.vert'] = CRT_VERT
        self.ctx.shaders['crt.frag'] = CRT_FRAG
        self.pipeline = self.ctx.pipeline(
            'crt.vert',
            'crt.frag',
            samplers={'Texture': 0},
            uniforms={
                'time': 'float',
                'scale': 'vec2',
                'offset': 'vec2',
                'screen_size': 'vec2',
                'color_shift': 'float',
                'color_mode': 'int',
                'enable_noise': 'int',
                'enable_scanline': 'int',
                'enable_multisample': 'int',
                'enable_screen': 'int',
            },
            vertex_array=self.ctx.empty_vertex_array,
            vertices=3,
            framebuffer=self.ctx.screen,
            resources=self.ctx.resources(
                samplers={
                    0: self.ctx.sampler(
                        self.texture,
                        wrap_x='clamp_to_edge',
                        wrap_y='clamp_to_edge',
                        min_filter='nearest',
                        mag_filter='nearest',
                    ),
                },
            ),
        )
        self.pipeline['scale'] = (1.0, 1.0)
        self.pipeline['offset'] = (0.0, 0.0)
        self.pipeline['screen_size'] = render_size
        self.pipeline['color_shift'] = 0.001
        self.pipeline['color_mode'] = 1
        self.pipeline['enable_noise'] = 1
        self.pipeline['enable_scanline'] = 1
        self.pipeline['enable_multisample'] = 1
        self.pipeline['enable_screen'] = 1

    def render(self, surface):
        self.texture.write(pygame.image.tobytes(surface, 'RGBA'))
        self.pipeline['time'] = pygame.time.get_ticks()
        self.ctx.start_frame()
        self.pipeline.run()
        self.ctx.end_frame()
